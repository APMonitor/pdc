% save as step_test.m
clear all; close all; clc

Q = 100.0; % Percent Heater (0-100%)
TK0 = 23.0 + 273.15; % Initial temperature
n = 60*10+1;  % Number of second time points (10min)
time = linspace(0,n-1,n); % Time vector
[time,TK] = ode23(@(t,x)heat(t,x,Q),time,TK0); % Integrate ODE

% Plot results
figure(1)
plot(time/60.0,TK-273.15,'b-')
ylabel('Temperature (degC)')
xlabel('Time (min)')
legend('Step Test (0-100% heater)')