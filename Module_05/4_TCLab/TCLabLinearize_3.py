import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
import tclab
import time 

n = 300  # Number of second time points (5 min)

# collect data if TCLab is connected
try:
    lab = tclab.TCLab()
    T1 = [lab.T1]
    lab.Q1(75)
    for i in range(n):
        time.sleep(1)
        print(lab.T1)
        T1.append(lab.T1)
    lab.close()
    connected = True
except:
    print('Connect TCLab to Get Data')
    connected = False

# simulation
U = 5.0
A = 0.0012
alpha = 0.01
eps = 0.9
sigma = 5.67e-8
Ta = 23
Cp = 500 
m = 0.004
Q = 75
TaK = Ta + 273.15
gamma = -U*A/(m*Cp) - 4*eps*sigma*A*TaK**3/(m*Cp)
beta = alpha/(m*Cp)
def labsim(x,t):
    TC,TC2 = x
    # convert to Kelvin
    TK = TC + 273.15
    # nonlinear
    dTCdt = (U*A*(Ta-TC) + sigma*eps*A*(TaK**4-TK**4) + alpha*Q)/(m*Cp)
    # linear
    dTC2dt = gamma * (TC2-23) + beta * (Q-0)
    return [dTCdt,dTC2dt]

tm = np.linspace(0,n,n+1) # Time values
Tsim = odeint(labsim,[23,23],tm)

T_nonlinear = Tsim[:,0]
T_linear = Tsim[:,1]

# Plot results
plt.figure()
plt.plot(tm,T_nonlinear,'b-',label='Nonlinear')
plt.plot(tm,T_linear,'k:',label='Linear')
if connected:
    plt.plot(tm,T1,'r.',label='Measured')
plt.ylabel(r'Temperature ($^oC$)')
plt.legend()
plt.xlabel('Time (sec)')
plt.show()