import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from scipy.optimize import minimize

# Import data file
# Column 1 = time (t)
# Column 2 = input (u)
# Column 3 = output (yp)
data = np.loadtxt('data.txt',delimiter=',',skiprows=1)
# initial conditions
Q0 = data[0,1]
Tmeas0 = data[0,3]
# extract data columns
t = data[:,0].T
Q = data[:,1].T
Tmeas = data[:,3].T

# specify number of steps
ns = len(t)
delta_t = t[1]-t[0]

Cp = 0.5 * 1000.0     # J/kg-K    
A = 12.0 / 100.0**2   # Area in m^2
Ta = Tmeas0           # Ambient temperature (K)

# define energy balance model
def heat(x,t,Q,p):
    # Adjustable Parameters
    U = p[0] # starting at 10.0 W/m^2-K
    alpha = p[1] # starting as 0.01 W / % heater

    # Known Parameters
    m = 4.0/1000.0     # kg
    Cp = 0.5 * 1000.0  # J/kg-K    
    A = 12.0 / 100.0**2 # Area in m^2
    eps = 0.9          # Emissivity
    sigma = 5.67e-8    # Stefan-Boltzman

    # Temperature State 
    T = x[0]

    # Nonlinear Energy Balance
    dTdt = (1.0/(m*Cp))*(U*A*(Ta-T) \
            + eps * sigma * A * (Ta**4 - T**4) \
            + alpha*Q)
    return dTdt

def calc_T(p):
    T = np.ones(len(t)) * Tmeas0
    T0 = T[0]
    for i in range(len(t)-1):
        ts = [t[i],t[i+1]]
        y = odeint(heat,T0,ts,args=(Q[i],p))
        T0 = y[-1]
        T[i+1] = T0
    return T

# define objective
def objective(p):
    # simulate model
    Tp = calc_T(p)
    # calculate objective
    obj = 0.0
    for i in range(len(Tmeas)):
        obj = obj + ((Tp[i]-Tmeas[i])/Tmeas[i])**2    
    # return result
    return obj

# Parameter initial guess
U = 10.0          # Heat transfer coefficient (W/m^2-K)
alpha = 0.01      # Heat gain (W/%)
p0 = [U,alpha]

# show initial objective
print('Initial SSE Objective: ' + str(objective(p0)))

# optimize parameters
# bounds on variables
bnds = ((2.0, 20.0),(0.005,0.02))
solution = minimize(objective,p0,method='SLSQP',bounds=bnds)
p = solution.x

# show final objective
print('Final SSE Objective: ' + str(objective(p)))

# optimized parameter values
U = p[0]
alpha = p[1]
print('U: ' + str(U))
print('alpha: ' + str(alpha))

# Known Parameters
m = 4.0/1000.0     # kg
Cp = 0.5 * 1000.0  # J/kg-K    
A = 12.0 / 100.0**2 # Area in m^2
eps = 0.9          # Emissivity
sigma = 5.67e-8    # Stefan-Boltzman
T0 = Tmeas0

print('')
print('FOPDT Equivalent')
#dx/dt = (-1/taup) * x + (Kp/taup) * u
#dTdt = (1.0/(m*Cp))*(-h*A*(T-Ta) + Amp*mVi/1000.0)
dfdT = -(U*A-4.0*eps*sigma*A*T0**3)/(m*Cp)
dfdQ = alpha/(m*Cp)
taup = -1.0/dfdT
Kp = dfdQ * taup
print('Kp: ' + str(Kp))
print('taup: ' + str(taup))

# calculate model with updated parameters
T1 = calc_T(p0)
T2 = calc_T(p)

# Plot the results
plt.figure()
plt.subplot(2,1,1)
plt.plot(t,Q,'k-',linewidth=3)
plt.ylabel('Heater')
plt.legend(['Heater'],loc='best')

plt.subplot(2,1,2)
plt.plot(t,T1,'b:',linewidth=3,label='Initial Guess')
plt.plot(t,Tmeas,'r-',linewidth=3,label='Measured')
plt.plot(t,T2,'k--',linewidth=3,label='Final Prediction')
plt.ylabel('Temperature (K)')
plt.legend(loc='best')
plt.xlabel('Time (sec)')
plt.savefig('optimization.png')
plt.show()