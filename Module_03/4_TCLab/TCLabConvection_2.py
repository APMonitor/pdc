import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
import tclab
import time

n = 300  # Number of second time points (5 min)
tm = np.linspace(0,n,n+1) # Time values

# data
lab = tclab.TCLab()
T1 = [lab.T1]
lab.Q1(50)
for i in range(n):
    time.sleep(1.0)
    print(lab.T1)
    T1.append(lab.T1)
lab.close()

# simulation
def labsim(TC,t):
    U = 10.0
    A = 0.0012
    Cp = 500 
    m = 0.004
    alpha = 0.01
    Ta = 23
    dTCdt = (U*A*(Ta-TC) + alpha*50)/(m*Cp)
    return dTCdt
Tsim = odeint(labsim,23,tm)

# Plot results
plt.figure(1)
plt.plot(tm,Tsim,'b-',label='Simulated')
plt.plot(tm,T1,'r.',label='Measured')
plt.ylabel('Temperature (degC)')
plt.xlabel('Time (sec)')
plt.legend()
plt.show()