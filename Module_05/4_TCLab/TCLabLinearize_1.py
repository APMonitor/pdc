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
TaK = Ta + 273.15
def labsim(TC,t):
    TK = TC + 273.15
    dTCdt = (U*A*(Ta-TC) + sigma*eps*A*(TaK**4-TK**4) + alpha*50)/(m*Cp)
    return dTCdt

tm = np.linspace(0,n,n+1) # Time values
Tsim = odeint(labsim,23,tm)

# calculate losses from conv and rad
conv = U*A*(Ta-Tsim)
rad = sigma*eps*A*(TaK**4-(Tsim+273.15)**4)
loss = conv+rad
gain = alpha*50

# Plot results
plt.figure()
plt.subplot(2,1,1)
plt.plot(tm,Tsim,'b-',label='Simulated')
if connected:
    plt.plot(tm,T1,'r.',label='Measured')
plt.ylabel(r'Temperature ($^oC$)')
plt.legend()
plt.subplot(2,1,2)
plt.plot(tm,conv,'g:',label='Convection')
plt.plot(tm,rad,'r--',label='Radiation')
plt.plot(tm,loss,'k-',label='Total Lost')
plt.text(150,-0.1,'Heater input = '+str(gain)+' W')
plt.ylabel(r'Heat Loss (W)')
plt.legend(loc=3)
plt.xlabel('Time (sec)')
plt.show()