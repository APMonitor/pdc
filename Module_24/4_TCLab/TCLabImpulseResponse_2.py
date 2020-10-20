import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import tclab
import time

try:
    # read Step_Response.csv if it exists
    data = pd.read_csv('Impulse_Response.csv')
    tm = data['Time'].values
    Q1 = data['Q1'].values
    T1 = data['T1'].values
except:
    # generate data only once
    n = 120  # Number of second time points (2 min)
    tm = np.linspace(0,n,n+1) # Time values
    lab = tclab.TCLab()
    T1 = [lab.T1]
    Q1 = np.zeros(n+1)
    Q1[10:71] = 70.0
    for i in range(n):
        lab.Q1(Q1[i])
        time.sleep(1)
        print(lab.T1)
        T1.append(lab.T1)
    lab.close()
    # Save data file
    data = np.vstack((tm,Q1,T1)).T
    np.savetxt('Impulse_Response.csv',data,delimiter=',',\
               header='Time,Q1,T1',comments='')

# Analytic solution
nt = len(tm)
Kp = 0.9
taup = 190.0
s1 = np.zeros(nt)
s1[25:] = 1.0
s2 = np.zeros(nt)
s2[85:] = 1.0
T1s = 70 * Kp * (1.0-np.exp(-(tm-25.0)/taup))*s1 - \
      70 * Kp * (1.0-np.exp(-(tm-85.0)/taup))*s2 + T1[0]

# Create Figure
plt.figure(figsize=(10,7))
ax = plt.subplot(2,1,1)
ax.grid()
plt.plot(tm,T1,'r.',label=r'$T_1$ measured')
plt.plot(tm,T1s,'b:',label=r'$T_1$ predicted')
plt.ylabel(r'Temp ($^oC$)')
plt.legend()
ax = plt.subplot(2,1,2)
ax.grid()
plt.plot(tm,Q1,'b-',label=r'$Q_1$')
plt.ylabel(r'Heater 1 (%)')
plt.xlabel('Time (sec)')
plt.legend()
plt.savefig('Impulse_Response.png')
plt.show()