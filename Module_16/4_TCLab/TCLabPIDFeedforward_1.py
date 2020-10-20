import numpy as np
import matplotlib.pyplot as plt
import tclab
import time

n = 600  # Number of second time points (10 min)
tm = np.linspace(0,n,n+1) # Time values

# data
lab = tclab.TCLab()
T1 = [lab.T1]
T2 = [lab.T2]
lab.Q2(100)
for i in range(n):
    time.sleep(1)
    print(lab.T1,lab.T2)
    T1.append(lab.T1)
    T2.append(lab.T2)
lab.close()

# Disturbance Gain
Kd = (T1[-1]-T1[0]) / (T2[-1]-T2[0])

# Plot results
plt.figure(1)
plt.plot(tm/60.0,T1,'r.',label=r'Measured $T_1$')
plt.plot(tm/60.0,T2,'b.',label=r'Measured $T_2$')
plt.text(3,40,'Disturbance Gain (Kd): '+str(round(Kd,2)))
plt.ylabel(r'Temperature ($^o$C)')
plt.xlabel('Time (min)')
plt.legend()
plt.savefig('Disturbance_gain.png')
plt.show()