import numpy as np
import matplotlib.pyplot as plt
import tclab
import time

n = 300  # Number of second time points (5 min)
tm = np.linspace(0,n,n+1) # Time values

Kp2 = 
taup2 = 
thetap2 = 
Tss = 23.0
Qstep = 65

# step response simulation
T2s = Kp2 * (1-np.exp(-(tm-thetap2)/taup2)) * Qstep
# time delay
step = np.zeros(n+1)
step[int(np.floor(thetap2)):]=1.0
T2s = T2s * step + Tss

# step response data
lab = tclab.TCLab()
T2 = [lab.T2]
lab.Q2(Qstep)
for i in range(n):
    time.sleep(1)
    print(i,lab.T2)
    T2.append(lab.T2)
lab.close()

# Plot results
plt.figure(figsize=(8,5))
plt.plot(tm,T2,'r.',label='Measured')
plt.plot(tm,T2s,'k-',label='Predicted')
plt.ylabel('Temperature (degC)')
plt.xlabel('Time (sec)')
plt.legend()
plt.savefig('Q2_step_test.png')
plt.show()