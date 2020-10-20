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
Q = m.Param(value=100.0) # Percent Heater (0-100%)

T0 = m.Param(value=23.0+273.15)     # Initial temperature
Ta = m.Param(value=23.0+273.15)     # K
U =  m.Param(value=10.0)            # W/m^2-K
mass = m.Param(value=4.0/1000.0)    # kg
Cp = m.Param(value=0.5*1000.0)      # J/kg-K    
A = m.Param(value=12.0/100.0**2)    # Area in m^2
alpha = m.Param(value=0.01)         # W / % heater
eps = m.Param(value=0.9)            # Emissivity
sigma = m.Const(5.67e-8)            # Stefan-Boltzman

T = m.Var(value=T0)         #Temperature state as GEKKO variable

m.Equation(T.dt() == (1.0/(mass*Cp))*(U*A*(Ta-T) \
                    + eps * sigma * A * (Ta**4 - T**4) \
                    + alpha*Q))

#simulation mode
m.options.IMODE = 4

#simulation model
m.solve()

#plot results
plt.figure(1)
plt.plot(m.time/60.0,np.array(T.value)-273.15,'b-')
plt.ylabel('Temperature (degC)')
plt.xlabel('Time (min)')
plt.legend(['Step Test (0-100% heater)'])
plt.show()