% save as heat.m
% define energy balance model
function dTdt = heat(time,x,Q)
    % Parameters
    Ta = 23 + 273.15;   % K
    U = 10.0;           % W/m^2-K
    m = 4.0/1000.0;     % kg
    Cp = 0.5 * 1000.0;  % J/kg-K    
    A = 12.0 / 100.0^2; % Area in m^2
    alpha = 0.01;       % W / % heater
    eps = 0.9;          % Emissivity
    sigma = 5.67e-8;    % Stefan-Boltzman

    % Temperature State 
    T = x(1);

    % Nonlinear Energy Balance
    dTdt = (1.0/(m*Cp))*(U*A*(Ta-T) ...
            + eps * sigma * A * (Ta^4 - T^4) ...
            + alpha*Q);
end