#load packages
import numpy as np
import matplotlib.pyplot as plt
from gekko import GEKKO

#initialize GEKKO model
m = GEKKO()

#model discretized time
n = 60*10+1  # Number of second time points (10min)
m.time = np.linspace(0,n-1,n) # Time vector

# Parameters
# Percent Heater (0-100%)
Q1v = np.zeros(n)
Q2v = np.zeros(n)
# Heater steps
Q1v[6:] = 100.0   # at 0.1 min (6 sec)
Q2v[300:] = 100.0 # at 5.0 min (300 sec)
# Heaters as time-varying inputs
Q1 = m.Param(value=Q1v) # Percent Heater (0-100%)
Q2 = m.Param(value=Q2v) # Percent Heater (0-100%)

T0 = m.Param(value=23.0+273.15)     # Initial temperature
Ta = m.Param(value=23.0+273.15)     # K
U =  m.Param(value=10.0)            # W/m^2-K
mass = m.Param(value=4.0/1000.0)    # kg
Cp = m.Param(value=0.5*1000.0)      # J/kg-K    
A = m.Param(value=10.0/100.0**2)    # Area not between heaters in m^2
As = m.Param(value=2.0/100.0**2)    # Area between heaters in m^2
alpha1 = m.Param(value=0.01)        # W / % heater
alpha2 = m.Param(value=0.0075)      # W / % heater
eps = m.Param(value=0.9)            # Emissivity
sigma = m.Const(5.67e-8)            # Stefan-Boltzman

# Temperature states as GEKKO variables
T1 = m.Var(value=T0)
T2 = m.Var(value=T0)         

# Between two heaters
Q_C12 = m.Intermediate(U*As*(T2-T1)) # Convective
Q_R12 = m.Intermediate(eps*sigma*As*(T2**4-T1**4)) # Radiative

m.Equation(T1.dt() == (1.0/(mass*Cp))*(U*A*(Ta-T1) \
                    + eps * sigma * A * (Ta**4 - T1**4) \
                    + Q_C12 + Q_R12 \
                    + alpha1*Q1))

m.Equation(T2.dt() == (1.0/(mass*Cp))*(U*A*(Ta-T2) \
                    + eps * sigma * A * (Ta**4 - T2**4) \
                    - Q_C12 - Q_R12 \
                    + alpha2*Q2))

#simulation mode
m.options.IMODE = 4

#simulation model
m.solve()

#plot results
plt.figure(1)
plt.subplot(2,1,1)
plt.plot(m.time/60.0,np.array(T1.value)-273.15,'b-')
plt.plot(m.time/60.0,np.array(T2.value)-273.15,'r--')
plt.legend([r'$T_1$',r'$T_2$'],loc='best')
plt.ylabel('Temperature (degC)')

plt.subplot(2,1,2)
plt.plot(m.time/60.0,np.array(Q1.value),'b-')
plt.plot(m.time/60.0,np.array(Q2.value),'r--')
plt.legend([r'$Q_1$',r'$Q_2$'],loc='best')
plt.ylabel('Heaters (%)')

plt.xlabel('Time (min)')
plt.show()