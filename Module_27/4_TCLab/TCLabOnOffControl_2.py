import matplotlib.pyplot as plt
import pandas as pd
data = pd.read_csv('data.csv')
plt.figure(figsize=(10,7))
ax=plt.subplot(2,1,1); ax.grid()
plt.plot(data['Time'],data['Q1'],'b-',label=r'$Q_1$ (%)')
plt.legend(); plt.ylabel('Heater')
ax=plt.subplot(2,1,2); ax.grid()
plt.plot(data['Time'],data['T1'],'r-',label=r'$T_1$ $(^oC)$')
plt.legend(); plt.xlabel('Time (sec)'); plt.ylabel('Temperature')
plt.show()