% define energy balance model
function dTdt = heat(t,x,Q1,Q2,p)
    %U = 10.0;           % W/m^2-K
    %alpha1 = 0.0100;    % W / % heater 1
    %alpha2 = 0.0075;    % W / % heater 2
    U = p(1);
    alpha1 = p(2);
    alpha2 = p(3);

    % Parameters
    Ta = 23 + 273.15;   % K
    m = 4.0/1000.0;     % kg
    Cp = 0.5 * 1000.0;  % J/kg-K    
    A = 10.0 / 100.0^2; % Area in m^2
    As = 2.0 / 100.0^2; % Area in m^2
    eps = 0.9;          % Emissivity
    sigma = 5.67e-8;    % Stefan-Boltzman

    % Temperature States 
    T1 = x(1)+273.15;
    T2 = x(2)+273.15;

    % Heat Transfer Exchange Between 1 and 2
    conv12 = U*As*(T2-T1);
    rad12  = eps*sigma*As * (T2^4 - T1^4);

    % Nonlinear Energy Balances
    dT1dt = (1.0/(m*Cp))*(U*A*(Ta-T1) ...
            + eps * sigma * A * (Ta^4 - T1^4) ...
            + conv12 + rad12 ...
            + alpha1*Q1);
    dT2dt = (1.0/(m*Cp))*(U*A*(Ta-T2) ...
            + eps * sigma * A * (Ta^4 - T2^4) ...
            - conv12 - rad12 ...
            + alpha2*Q2);
    dTdt = [dT1dt,dT2dt]';
end