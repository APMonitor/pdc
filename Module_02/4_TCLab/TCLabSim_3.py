import numpy as np
import matplotlib.pyplot as plt
import tclab
import time
# pip install gekko
from gekko import GEKKO 

n = 300  # Number of second time points (5 min)

# data
lab = tclab.TCLab()
T1 = [lab.T1]
lab.Q1(50)
for i in range(n):
    time.sleep(1)
    print(lab.T1)
    T1.append(lab.T1)
lab.close()

# simulation
m = GEKKO()
m.time = np.linspace(0,n,n+1)
TC = m.Var(23)
m.Equation(120*TC.dt()==(23-TC)+0.8*50)
m.options.IMODE = 4 # dynamic simulation
m.solve(disp=False)

# Plot results
plt.figure(1)
plt.plot(m.time,TC,'b-',label='Simulated')
plt.plot(m.time,T1,'r.',label='Measured')
plt.ylabel('Temperature (degC)')
plt.xlabel('Time (sec)')
plt.legend()
plt.show()