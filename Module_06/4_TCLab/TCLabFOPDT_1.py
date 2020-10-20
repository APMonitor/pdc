import numpy as np
import matplotlib.pyplot as plt
import tclab
import time

n = 480  # Number of second time points (8 min)
tm = np.linspace(0,n,n+1) # Time values

# data
lab = tclab.TCLab()
T1 = [lab.T1]
Q1 = np.zeros(n+1)
Q1[30:] = 70.0
for i in range(n):
    lab.Q1(Q1[i])
    time.sleep(1)
    print(lab.T1)
    T1.append(lab.T1)
lab.close()

# Create Figure
plt.figure(figsize=(12,8))
ax = plt.subplot(2,1,1)
ax.grid()
plt.plot(tm/60.0,T1,'r.',label=r'$T_1$')
plt.ylabel(r'Temp ($^oC$)')
ax = plt.subplot(2,1,2)
ax.grid()
plt.plot(tm/60.0,Q1,'b-',label=r'$Q_1$')
plt.ylabel(r'Heater (%)')
plt.xlabel('Time (min)')
plt.legend()
plt.savefig('Step_Response.png')
plt.show()