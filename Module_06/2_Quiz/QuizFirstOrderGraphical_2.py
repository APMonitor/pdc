import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from scipy.interpolate import interp1d

# define first-order plus dead-time approximation    
def fopdt(y,t,uf,Km,taum,thetam):
    # arguments
    #  y      = output
    #  t      = time
    #  uf     = input linear function (for time shift)
    #  Km     = model gain
    #  taum   = model time constant
    #  thetam = model time constant
    # time-shift u
    try:
        if (t-thetam) <= 0:
            um = uf(0.0)
        else:
            um = uf(t-thetam)
    except:
        um = 0
    # calculate derivative
    dydt = (-y + Km * um)/taum
    return dydt

# specify number of steps
ns = 150
# define time points
t = np.linspace(0,15,ns+1)
delta_t = t[1]-t[0]
# define input vector
u = np.zeros(ns+1)
u[10:] = -2.0
# create linear interpolation of the u data versus time
uf = interp1d(t,u)

# simulate FOPDT model with x=[Km,taum,thetam]
def sim_model(Km,taum,thetam):
    # input arguments
    #Km 
    #taum 
    #thetam 
    # storage for model values
    ym = np.zeros(ns+1)  # model
    # initial condition
    ym[0] = 0
    # loop through time steps    
    for i in range(1,ns+1):
        ts = [delta_t*(i-1),delta_t*i]
        y1 = odeint(fopdt,ym[i-1],ts,args=(uf,Km,taum,thetam))
        ym[i] = y1[-1]
    return ym    

# calculate model with updated parameters
Km = 2.0
taum = 2.0
thetam = 2.0
ym = sim_model(Km,taum,thetam)

# plot results
plt.figure()
plt.subplot(2,1,1)
plt.plot(t,u,'b-',linewidth=2)
plt.legend(['u'],loc='best')
plt.ylabel('Input Step (u)')
plt.grid()
plt.subplot(2,1,2)
plt.plot(t,ym,'k--',linewidth=2,label='y')
plt.ylabel('Output Response (y)')
plt.legend(loc='best')
plt.xlabel('Time (sec)')
plt.grid()
plt.show()