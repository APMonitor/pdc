close all; clear all; clc

global t T1meas T2meas Q1 Q2

% generate data file from TCLab or get sample data file from:
%  https://apmonitor.com/pdc/index.php/Main/ArduinoEstimation2
% Import data file
% Column 1 = time (t)
% Column 2 = input (u)
% Column 3 = output (yp)
filename = 'data.txt';
delimiterIn = ',';
headerlinesIn = 1;
z = importdata(filename,delimiterIn,headerlinesIn);
% extract data columns
t = z.data(:,1);
Q1 = z.data(:,2);
Q2 = z.data(:,3);
T1meas = z.data(:,4);
T2meas = z.data(:,5);

% number of time points
ns = length(t);

% Parameter initial guess
U = 10.0;           % Heat transfer coefficient (W/m^2-K)
alpha1 = 0.0100;    % Heat gain 1 (W/%)
alpha2 = 0.0075;    % Heat gain 2 (W/%)
p0 = [U,alpha1,alpha2];

% show initial objective
disp(['Initial SSE Objective: ' num2str(objective(p0))])

% optimize parameters

% no linear constraints
A = [];
b = [];
Aeq = [];
beq = [];
nlcon = [];

% optimize with fmincon
lb = [2,0.005,0.002]; % lower bound
ub = [20,0.02,0.015]; % upper bound
% options = optimoptions(@fmincon,'Algorithm','interior-point');
p = fmincon(@objective,p0,A,b,Aeq,beq,lb,ub,nlcon); %,options);

% show final objective
disp(['Final SSE Objective: ' num2str(objective(p))])

% optimized parameter values
U = p(1);
alpha1 = p(2);
alpha2 = p(3);
disp(['U: ' num2str(U)])
disp(['alpha1: ' num2str(alpha1)])
disp(['alpha2: ' num2str(alpha2)])

% calculate model with updated parameters
Ti  = simulate(p0);
Tp  = simulate(p);

% Plot results
figure(1)

subplot(3,1,1)
plot(t/60.0,Ti(:,1),'y:','LineWidth',2)
hold on
plot(t/60.0,T1meas,'b-','LineWidth',2)
plot(t/60.0,Tp(:,1),'r--','LineWidth',2)
ylabel('Temperature (degC)')
legend('T_1 initial','T_1 measured','T_1 optimized')

subplot(3,1,2)
plot(t/60.0,Ti(:,2),'y:','LineWidth',2)
hold on
plot(t/60.0,T2meas,'b-','LineWidth',2)
plot(t/60.0,Tp(:,2),'r--','LineWidth',2)
ylabel('Temperature (degC)')
legend('T_2 initial','T_2 measured','T_2 optimized')

subplot(3,1,3)
plot(t/60.0,Q1,'g-','LineWidth',2)
hold on
plot(t/60.0,Q2,'k--','LineWidth',2)
ylabel('Heater Output')
legend('Q_1','Q_2')

xlabel('Time (min)')