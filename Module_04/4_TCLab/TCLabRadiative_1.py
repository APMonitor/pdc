import numpy as np
import matplotlib.pyplot as plt
import tclab
import time

n = 300  # Number of second time points (5 min)
tm = np.linspace(0,n,n+1) # Time values

# data
lab = tclab.TCLab()
T1 = [lab.T1]
lab.Q1(50)
for i in range(n):
    time.sleep(1)
    print(lab.T1)
    T1.append(lab.T1)
lab.close()

# Plot results
plt.figure(1)
plt.plot(tm,T1,'r.',label='Measured')
plt.ylabel('Temperature (degC)')
plt.xlabel('Time (sec)')
plt.legend()
plt.show()