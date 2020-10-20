import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

data = pd.read_csv('data.csv')

# graphical fit
Delta_SP = 20
Delta_T1 = 21
OS = (44-41)/(41-20)
tp = 86.0
Kp = Delta_T1/Delta_SP
lnOS2 = (np.log(OS))**2
zeta = np.sqrt(lnOS2/(np.pi**2+lnOS2))
taus = tp * np.sqrt(1-zeta**2)/np.pi
print('Kp: ' + str(Kp))
print('zeta: ' + str(zeta))
print('taus: ' + str(taus))

# analytic solution
t = data['Time'].values
T0 = data['T1'].values[0]
a = np.sqrt(1-zeta**2)
b = t/taus
c = np.cos(a*b)
d = (zeta/a)*np.sin(a*b)
T1 = Kp*Delta_SP*(1-np.exp(-zeta*b)*(c+d))+T0

plt.figure(figsize=(10,7))
ax=plt.subplot(2,1,1); ax.grid()
plt.plot(data['Time'],data['Q1'],'b-',label=r'$Q_1$ (%)')
plt.legend(); plt.ylabel('Heater')
ax=plt.subplot(2,1,2); ax.grid()
plt.plot(data['Time'],data['T1'],'r-',label=r'$T_1$ Meas $(^oC)$')
plt.plot(t,T1,'k:',label=r'$T_1$ Pred $(^oC)$')
plt.legend(); plt.xlabel('Time (sec)'); plt.ylabel('Temperature')
plt.show()