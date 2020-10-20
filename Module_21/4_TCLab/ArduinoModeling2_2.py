clear all; close all; clc

n = 60*10+1;  % Number of second time points (10min)

% Percent Heater (0-100%)
Q1 = zeros(n,1);
Q2 = zeros(n,1);
% Heater steps
Q1(7:end) = 100.0;   % at 0.1 min (6 sec)
Q2(301:end) = 100.0; % at 5.0 min (300 sec)

% Initial temperature
T0 = 23.0 + 273.15;

% Store temperature results
T1 = ones(n,1)*T0;
T2 = ones(n,1)*T0;

time = linspace(0,n-1,n); % Time vector

for i = 2:n
    % initial condition for next step
    x0 = [T1(i-1),T2(i-1)];
    % time interval for next step
    tm = [time(i-1),time(i)];
    % Integrate ODE for 1 sec each loop
    z = ode45(@(t,x)heat2(t,x,Q1(i-1),Q2(i-1)),tm,x0);
    % record T1 and T2 at end of simulation
    T1(i) = z.y(1,end);
    T2(i) = z.y(2,end);
end

% Plot results
figure(1)

subplot(2,1,1)
plot(time/60.0,T1-273.15,'b-','LineWidth',2)
hold on
plot(time/60.0,T2-273.15,'r--','LineWidth',2)
ylabel('Temperature (degC)')
legend('T_1','T_2')

subplot(2,1,2)
plot(time/60.0,Q1,'b-','LineWidth',2)
hold on
plot(time/60.0,Q2,'r--','LineWidth',2)
ylabel('Heater Output')
legend('Q_1','Q_2')
ylim([-10,110])
xlabel('Time (min)')