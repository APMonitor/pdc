import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
%matplotlib inline
from scipy.integrate import odeint
from scipy.optimize import minimize
from scipy.interpolate import interp1d

# initial guesses
x0 = np.zeros(4)
x0[0] = 0.8 # Kp
x0[1] = 0.2 # Kd
x0[2] = 150.0 # taup
x0[3] = 10.0 # thetap

# Import CSV data file
# try to read local data file first
try:
    filename = 'data.csv'
    data = pd.read_csv(filename)
except:
    filename = 'http://apmonitor.com/pdc/uploads/Main/tclab_data2.txt'
    data = pd.read_csv(filename)
Q1_0 = data['Q1'].values[0]
Q2_0 = data['Q2'].values[0]
T1_0 = data['T1'].values[0]
T2_0 = data['T2'].values[0]
t = data['Time'].values - data['Time'].values[0]
Q1 = data['Q1'].values
Q2 = data['Q2'].values
T1 = data['T1'].values
T2 = data['T2'].values

# specify number of steps
ns = len(t)
delta_t = t[1]-t[0]
# create linear interpolation of the u data versus time
Qf1 = interp1d(t,Q1)
Qf2 = interp1d(t,Q2)

# define first-order plus dead-time approximation    
def fopdt(T,t,Qf1,Qf2,Kp,Kd,taup,thetap):
    #  T      = states
    #  t      = time
    #  Qf1    = input linear function (for time shift)
    #  Qf2    = input linear function (for time shift)
    #  Kp     = model gain
    #  Kd     = disturbance gain
    #  taup   = model time constant
    #  thetap = model time constant
    # time-shift Q
    try:
        if (t-thetap) <= 0:
            Qm1 = Qf1(0.0)
            Qm2 = Qf2(0.0)
        else:
            Qm1 = Qf1(t-thetap)
            Qm2 = Qf2(t-thetap)
    except:
        Qm1 = Q1_0
        Qm2 = Q2_0
    # calculate derivative
    dT1dt = (-(T[0]-T1_0) + Kp*(Qm1-Q1_0) + Kd*(T[1]-T[0]))/taup
    dT2dt = (-(T[1]-T2_0) + (Kp/2.0)*(Qm2-Q2_0) + Kd*(T[0]-T[1]))/taup
    return [dT1dt,dT2dt]

# simulate FOPDT model
def sim_model(x):
    # input arguments
    Kp,Kd,taup,thetap = x
    # storage for model values
    T1p = np.ones(ns) * T1_0
    T2p = np.ones(ns) * T2_0
    # loop through time steps    
    for i in range(0,ns-1):
        ts = [t[i],t[i+1]]
        T = odeint(fopdt,[T1p[i],T2p[i]],ts,args=(Qf1,Qf2,Kp,Kd,taup,thetap))
        T1p[i+1] = T[-1,0]
        T2p[i+1] = T[-1,1]
    return T1p,T2p

# define objective
def objective(x):
    # simulate model
    T1p,T2p = sim_model(x)
    # return objective
    return sum(np.abs(T1p-T1)+np.abs(T2p-T2))

# show initial objective
print('Initial SSE Objective: ' + str(objective(x0)))
print('Optimizing Values...')

# optimize without parameter constraints
#solution = minimize(objective,x0)

# optimize with bounds on variables
bnds = ((0.4, 1.5), (0.1, 0.5), (50.0, 200.0), (0.0, 30.0))
solution = minimize(objective,x0,bounds=bnds,method='SLSQP')

# show final objective
x = solution.x
iae = objective(x)
Kp,Kd,taup,thetap = x
print('Final SSE Objective: ' + str(objective(x)))
print('Kp: ' + str(Kp))
print('Kd: ' + str(Kd))
print('taup: ' + str(taup))
print('thetap: ' + str(thetap))
# save fopdt.txt file
fid = open('fopdt.txt','w')
fid.write(str(Kp)+'\n')
fid.write(str(Kd)+'\n')
fid.write(str(taup)+'\n')
fid.write(str(thetap)+'\n')
fid.write(str(T1_0)+'\n')
fid.write(str(T2_0)+'\n')
fid.close()

# calculate model with updated parameters
T1p,T2p = sim_model(x)

plt.figure(1,figsize=(15,7))
plt.subplot(2,1,1)
plt.plot(t,T1,'r.',linewidth=2,label='Temperature 1 (meas)')
plt.plot(t,T2,'b.',linewidth=2,label='Temperature 2 (meas)')
plt.plot(t,T1p,'r--',linewidth=2,label='Temperature 1 (pred)')
plt.plot(t,T2p,'b--',linewidth=2,label='Temperature 2 (pred)')
plt.ylabel(r'T $(^oC)$')
plt.text(200,20,'Integral Abs Error: ' + str(np.round(iae,2)))
plt.text(400,35,r'$K_p$: ' + str(np.round(Kp,2)))  
plt.text(400,30,r'$K_d$: ' + str(np.round(Kd,2)))  
plt.text(400,25,r'$\tau_p$: ' + str(np.round(taup,1)) + ' sec')  
plt.text(400,20,r'$\theta_p$: ' + str(np.round(thetap,1)) + ' sec')  
plt.legend(loc=2)
plt.subplot(2,1,2)
plt.plot(t,Q1,'b--',linewidth=2,label=r'Heater 1 ($Q_1$)')
plt.plot(t,Q2,'r:',linewidth=2,label=r'Heater 2 ($Q_2$)')
plt.legend(loc='best')
plt.xlabel('time (sec)')
plt.show()