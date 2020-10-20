import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from scipy.optimize import minimize
import pandas as pd

# generate data file from TCLab or get sample data file from:
#  https://apmonitor.com/pdc/index.php/Main/ArduinoEstimation2
# Import data file
# Column 1 = time (t)
# Column 2 = input (u)
# Column 3 = output (yp)
data = np.loadtxt('data.txt',delimiter=',',skiprows=1)
# extract data columns
t = data[:,0].T
Q1 = data[:,1].T
Q2 = data[:,2].T
T1meas = data[:,3].T
T2meas = data[:,4].T

# number of time points
ns = len(t)

# define energy balance model
def heat(x,t,Q1,Q2,p):
    # Optimized parameters
    U,alpha1,alpha2 = p

    # Parameters
    Ta = 23 + 273.15   # K
    m = 4.0/1000.0     # kg
    Cp = 0.5 * 1000.0  # J/kg-K    
    A = 10.0 / 100.0**2 # Area in m^2
    As = 2.0 / 100.0**2 # Area in m^2
    eps = 0.9          # Emissivity
    sigma = 5.67e-8    # Stefan-Boltzman

    # Temperature States 
    T1 = x[0] + 273.15
    T2 = x[1] + 273.15

    # Heat Transfer Exchange Between 1 and 2
    conv12 = U*As*(T2-T1)
    rad12  = eps*sigma*As * (T2**4 - T1**4)

    # Nonlinear Energy Balances
    dT1dt = (1.0/(m*Cp))*(U*A*(Ta-T1) \
            + eps * sigma * A * (Ta**4 - T1**4) \
            + conv12 + rad12 \
            + alpha1*Q1)
    dT2dt = (1.0/(m*Cp))*(U*A*(Ta-T2) \
            + eps * sigma * A * (Ta**4 - T2**4) \
            - conv12 - rad12 \
            + alpha2*Q2)

    return [dT1dt,dT2dt]

def simulate(p):
    T = np.zeros((len(t),2))
    T[0,0] = T1meas[0]
    T[0,1] = T2meas[0]    
    T0 = T[0]
    for i in range(len(t)-1):
        ts = [t[i],t[i+1]]
        y = odeint(heat,T0,ts,args=(Q1[i],Q2[i],p))
        T0 = y[-1]
        T[i+1] = T0
    return T

# define objective
def objective(p):
    # simulate model
    Tp = simulate(p)
    # calculate objective
    obj = 0.0
    for i in range(len(t)):
        obj += ((Tp[i,0]-T1meas[i])/T1meas[i])**2 \
              +((Tp[i,1]-T2meas[i])/T2meas[i])**2
    # return result
    return obj

# Parameter initial guess
U = 10.0           # Heat transfer coefficient (W/m^2-K)
alpha1 = 0.0100    # Heat gain 1 (W/%)
alpha2 = 0.0075    # Heat gain 2 (W/%)
p0 = [U,alpha1,alpha2]

# show initial objective
print('Initial SSE Objective: ' + str(objective(p0)))

# optimize parameters
# bounds on variables
bnds = ((2.0, 20.0),(0.005,0.02),(0.002,0.015))
solution = minimize(objective,p0,method='SLSQP',bounds=bnds)
p = solution.x

# show final objective
print('Final SSE Objective: ' + str(objective(p)))

# optimized parameter values
U = p[0]
alpha1 = p[1]
alpha2 = p[2]
print('U: ' + str(U))
print('alpha1: ' + str(alpha1))
print('alpha2: ' + str(alpha2))

# calculate model with updated parameters
Ti  = simulate(p0)
Tp  = simulate(p)

# Plot results
plt.figure(1)

plt.subplot(3,1,1)
plt.plot(t/60.0,Ti[:,0],'y:',label=r'$T_1$ initial')
plt.plot(t/60.0,T1meas,'b-',label=r'$T_1$ measured')
plt.plot(t/60.0,Tp[:,0],'r--',label=r'$T_1$ optimized')
plt.ylabel('Temperature (degC)')
plt.legend(loc='best')

plt.subplot(3,1,2)
plt.plot(t/60.0,Ti[:,1],'y:',label=r'$T_2$ initial')
plt.plot(t/60.0,T2meas,'b-',label=r'$T_2$ measured')
plt.plot(t/60.0,Tp[:,1],'r--',label=r'$T_2$ optimized')
plt.ylabel('Temperature (degC)')
plt.legend(loc='best')

plt.subplot(3,1,3)
plt.plot(t/60.0,Q1,'g-',label=r'$Q_1$')
plt.plot(t/60.0,Q2,'k--',label=r'$Q_2$')
plt.ylabel('Heater Output')
plt.legend(loc='best')

plt.xlabel('Time (min)')
plt.show()