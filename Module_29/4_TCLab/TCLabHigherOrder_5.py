import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from gekko import GEKKO
import tclab
import time
from scipy import signal

# Import data
try:
    # try to read local data file first
    filename = 'data.csv'
    data = pd.read_csv(filename)
except:
    filename = 'https://apmonitor.com/pdc/uploads/Main/tclab_data3.txt'
# read either local file or web file
data = pd.read_csv(filename)

U = 4.7052403301
Us = 15.45761703
alpha1 = 0.012321367852
alpha2 = 0.005
tau = 20.298826743
Ta = 293.15
mass = 0.004
Cp = 500.0
A = 0.001
As = 0.0002
eps = 0.9
sigma = 5.67e-08

Am = np.zeros((3,3))
Bm = np.zeros((3,1))
Cm = np.zeros((1,3))
Dm = np.zeros((1,1))

T0 = Ta
c1 = U*A
c2 = 4*eps*sigma*A*T0**3
c3 = Us*As
c4 = 4*eps*sigma*As*T0**3
c5 = mass*Cp
c6 = 1/tau

Am[0,0] = -(c1+c2+c3+c4)/c5
Am[0,1] = (c3+c4)/c5

Am[1,0] = (c3+c4)/c5
Am[1,1] = -(c1+c2+c3+c4)/c5

Am[2,1] = c6
Am[2,2] = -c6

Bm[0,0] = alpha1/c5

Cm[0,2] = 1

# state space simulation
ss = GEKKO()
x,y,u = ss.state_space(Am,Bm,Cm,D=None)
u[0].value = data['Q1'].values
ss.time = data['Time'].values
ss.options.IMODE = 7
ss.solve(disp=False)

# state space simulation with scipy
sys = signal.StateSpace(Am,Bm,Cm,Dm)
tsys = data['Time'].values
Qsys = data['Q1'].values.T
tsys,ysys,xsys = signal.lsim(sys,Qsys,tsys)

# print linearized models
print('State Space Model')
print(sys)

print('Transfer Function Model')
tf=sys.to_tf()
print(tf)

# Time series model
ts = GEKKO()
tt = data['Time'].values
tu = data['Q1'].values
ty = data['T2'].values
na = 5 # output coefficients
nb = 5 # input coefficients
print('Identify time series model')
# diaglevel = 1 option to see solver output
yp,p,K = ts.sysid(tt,tu,ty,na,nb,pred='model',objf=1000,diaglevel=0)

# Create plot
plt.figure(figsize=(10,7))
ax=plt.subplot(2,1,1)
ax.grid()
plt.plot(data['Time'],data['T2'],'b.',label=r'$T_2$ measured')
plt.plot(ss.time,np.array(y[0].value)+data['T2'][0],color='purple',linestyle=':',\
         linewidth=2,label=r'$T_2$ state space')
plt.plot(tt,yp,'g--',\
         linewidth=2,label=r'$T_2$ time series')
plt.ylabel(r'T ($^oC$)')
plt.legend(loc=2)
ax=plt.subplot(2,1,2)
ax.grid()
plt.plot(data['Time'],data['Q1'],'r-',\
         linewidth=3,label=r'$Q_1$')
plt.ylabel('Heater (%)')
plt.xlabel('Time (sec)')
plt.legend(loc='best')
plt.savefig('tclab_higher_order.png')
plt.show()