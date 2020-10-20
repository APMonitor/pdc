import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

# define thermocouple model
def thermocouple(x,t,Tg,Tf):
    ## States
    Tt = x[0] 
    Tlin = x[1]

    ## Parameters
    h = 2800.0            # W/m^2-K
    rho = 20.0            # gm/cm^3
    sigma = 5.67e-8       # W/m^2-K^4
    eps = 0.8             #
    Cp = 0.4              # J/gm-K    
    d = 0.01              # cm
    r = d / 2.0           # radius
    A = 4.0 * np.pi * (r/100.0)**2 # sphere area (m^2)
    V = 4.0/3.0 * np.pi * r**3 # sphere volume (cm^3)

    # acc = inlet - outlet
    # acc = m * Cp * dT/dt = rho * V * Cp * dT/dt
    # inlet - outlet from 2 heat transfer pathways
    # q(convection) = h * A * (Tg-Tt)
    # q(radiation) = A * esp * sigma * (Tf^4 - Tt^4)
    q_conv = h * A * (Tg-Tt)
    q_rad = A * eps * sigma * (Tf**4 - Tt**4)
    dTdt = (q_conv + q_rad) / (rho * V * Cp)
    dTlin_dt = 0.0 # add linearized equation
    return [dTdt,dTlin_dt]

# Flame temperature
Tf0 = 1500.0 #K

# Starting thermocouple temperature
y0 = [Tf0,Tf0]

# Time Intervals (sec)
t = np.linspace(0,0.1,1000)

# Flame Temperature
Tf = np.ones(len(t))*Tf0
Tf[500:] = 1520.0 #K

# Gas temperature cycles
Tg = Tf + (150.0/2.0) * np.sin(2.0 * np.pi * 100.0 * t) #K

# Store thermocouple temperature for plotting
Tt = np.ones(len(t)) * Tf
Tlin = np.ones(len(t)) * Tf

for i in range(len(t)-1):
    ts = [t[i],t[i+1]]
    y = odeint(thermocouple,y0,ts,args=(Tg[i],Tf[i]))
    y0 = y[-1]
    Tt[i+1] = y0[0]
    Tlin[i+1] = y0[1]

# Plot the results
plt.figure()
plt.plot(t,Tg,'b--',linewidth=3,label='Gas Temperature')
plt.plot(t,Tf,'g:',linewidth=3,label='Flame Temperature')
plt.plot(t,Tt,'r-',linewidth=3,label='Thermocouple')
plt.ylabel('Temperature (K)')
plt.legend(loc='best')
plt.xlim([0,t[-1]])
plt.xlabel('Time (sec)')

plt.show()