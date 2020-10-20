import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

# define energy balance model
def heat(x,t,Q1,Q2):
    # Parameters
    Ta = 23 + 273.15   # K
    U = 10.0           # W/m^2-K
    m = 4.0/1000.0     # kg
    Cp = 0.5 * 1000.0  # J/kg-K    
    A = 10.0 / 100.0**2 # Area in m^2
    As = 2.0 / 100.0**2 # Area in m^2
    alpha1 = 0.0100     # W / % heater 1
    alpha2 = 0.0075     # W / % heater 2
    eps = 0.9          # Emissivity
    sigma = 5.67e-8    # Stefan-Boltzman

    # Temperature States 
    T1 = x[0]
    T2 = x[1]

    # Heat Transfer Exchange Between 1 and 2
    conv12 = U*As*(T2-T1)
    rad12  = eps*sigma*As * (T2**4 - T1**4)

    # Nonlinear Energy Balances
    dT1dt = (1.0/(m*Cp))*(U*A*(Ta-T1) \
            + eps * sigma * A * (Ta**4 - T1**4) \
            + conv12 + rad12 \
            + alpha1*Q1)
    dT2dt = (1.0/(m*Cp))*(U*A*(Ta-T2) \
            + eps * sigma * A * (Ta**4 - T2**4) \
            - conv12 - rad12 \
            + alpha2*Q2)

    return [dT1dt,dT2dt]

n = 60*10+1  # Number of second time points (10min)

# Percent Heater (0-100%)
Q1 = np.zeros(n)
Q2 = np.zeros(n)
# Heater steps
Q1[6:] = 100.0   # at 0.1 min (6 sec)
Q2[300:] = 100.0 # at 5.0 min (300 sec)

# Initial temperature
T0 = 23.0 + 273.15 

# Store temperature results
T1 = np.ones(n)*T0
T2 = np.ones(n)*T0

time = np.linspace(0,n-1,n) # Time vector

for i in range(1,n):
    # initial condition for next step
    x0 = [T1[i-1],T2[i-1]]
    # time interval for next step
    tm = [time[i-1],time[i]]
    # input heaters for next step
    heaters = (Q1[i-1],Q2[i-1])
    # Integrate ODE for 1 sec each loop
    x = odeint(heat,x0,tm,args=heaters)
    # record T1 and T2 at end of simulation
    T1[i] = x[-1][0]
    T2[i] = x[-1][1]

# Plot results
plt.figure(1)

plt.subplot(2,1,1)
plt.plot(time/60.0,T1-273.15,'b-',label=r'$T_1$')
plt.plot(time/60.0,T2-273.15,'r--',label=r'$T_2$')
plt.ylabel('Temperature (degC)')
plt.legend(loc='best')

plt.subplot(2,1,2)
plt.plot(time/60.0,Q1,'b-',label=r'$Q_1$')
plt.plot(time/60.0,Q2,'r--',label=r'$Q_2$')
plt.ylabel('Heater Output')
plt.legend(loc='best')

plt.xlabel('Time (min)')
plt.show()