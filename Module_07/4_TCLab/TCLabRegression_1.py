import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import tclab
import time

try:
    # read Step_Response.csv if it exists
    data = pd.read_csv('Step_Response.csv')
    tm = data['Time'].values
    Q1 = data['Q1'].values
    T1 = data['T1'].values
except:
    # generate data only once
    n = 840  # Number of second time points (14 min)
    tm = np.linspace(0,n,n+1) # Time values
    lab = tclab.TCLab()
    T1 = [lab.T1]
    Q1 = np.zeros(n+1)
    Q1[30:] = 35.0
    Q1[270:] = 70.0
    Q1[450:] = 10.0
    Q1[630:] = 60.0
    Q1[800:] = 0.0
    for i in range(n):
        lab.Q1(Q1[i])
        time.sleep(1)
        print(lab.T1)
        T1.append(lab.T1)
    lab.close()
    # Save data file
    data = np.vstack((tm,Q1,T1)).T
    np.savetxt('Step_Response.csv',data,delimiter=',',\
               header='Time,Q1,T1',comments='')

# Create Figure
plt.figure(figsize=(10,7))
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