import numpy as np
%matplotlib inline
import matplotlib.pyplot as plt
from scipy.integrate import odeint
import ipywidgets as wg
from IPython.display import display

n = 601 # time points to plot
tf = 600.0 # final time

# TCLab Second-Order
Kp = 0.8473
taus = 51.08
zeta = 1.581
thetap = 0.0

def process(z,t,u):
    x,y = z
    dxdt = (1.0/(taus**2)) * (-2.0*zeta*taus*x-(y-23.0) + Kp * u)
    dydt = x
    return [dxdt,dydt]

def pidPlot(Kc):
    t = np.linspace(0,tf,n) # create time vector
    P = np.zeros(n)         # initialize proportional term
    e = np.zeros(n)         # initialize error
    OP = np.zeros(n)        # initialize controller output
    PV = np.ones(n)*23.0    # initialize process variable
    SP = np.ones(n)*23.0    # initialize setpoint
    SP[10:] = 60.0          # step up
    z0 = [0,23.0]           # initial condition
    # loop through all time steps
    for i in range(1,n):
        # simulate process for one time step
        ts = [t[i-1],t[i]]         # time interval
        z = odeint(process,z0,ts,args=(OP[max(0,i-1-int(thetap))],))
        z0 = z[1]                  # record new initial condition
        # calculate new OP with PID
        PV[i] = z0[1]              # record PV
        e[i] = SP[i] - PV[i]       # calculate error = SP - PV
        dt = t[i] - t[i-1]         # calculate time step
        P[i] = Kc * e[i]           # calculate proportional term
        OP[i] = min(100,max(0,P[i])) # calculate new controller output        

    P = np.zeros(n)         # initialize proportional term
    e = np.zeros(n)         # initialize error
    OPu = np.zeros(n)       # initialize controller output
    PVu = np.ones(n)*23.0   # initialize process variable
    SP = np.ones(n)*23.0    # initialize setpoint
    SP[10:] = 60.0          # step up
    z0 = [0,23.0]           # initial condition
    # loop through all time steps
    for i in range(1,n):
        # simulate process for one time step
        ts = [t[i-1],t[i]]         # time interval
        z = odeint(process,z0,ts,args=(OPu[max(0,i-1-int(thetap))],))
        z0 = z[1]                  # record new initial condition
        # calculate new OP with PID
        PVu[i] = z0[1]             # record PV
        e[i] = SP[i] - PVu[i]       # calculate error = SP - PV
        dt = t[i] - t[i-1]         # calculate time step
        P[i] = Kc * e[i]           # calculate proportional term
        OPu[i] = P[i]               # calculate new controller output

    # plot PID response
    plt.figure(1,figsize=(15,5))
    plt.subplot(1,2,1)
    plt.plot(t,SP,'k-',linewidth=2,label='Setpoint (SP)')
    plt.plot(t,PV,'r-',linewidth=2,label='Temperature - OP Limits (PV)')
    plt.plot(t,PVu,'b--',linewidth=2,label='Temperature - No OP Limits (PV)')
    plt.ylabel(r'T $(^oC)$')
    plt.text(100,30,'OP Limit Offset: ' + str(np.round(SP[-1]-PVu[-1],2)))
    M = SP[-1]-SP[0]
    pred_offset = M*(1-Kp*Kc/(1+Kp*Kc))
    plt.text(100,25,'No OP Limit Offset: ' + str(np.round(pred_offset,2)))
    plt.text(400,30,r'$K_c$: ' + str(np.round(Kc,1)))  
    plt.legend(loc=1)
    plt.xlabel('time (sec)')
    plt.subplot(1,2,2)
    plt.plot(t,OP,'r-',linewidth=2,label='Heater - OP Limits (OP)')
    plt.plot(t,OPu,'b--',linewidth=2,label='Heater - No OP Limits (OP)')
    plt.ylabel('Heater (%)')
    plt.legend(loc='best')
    plt.xlabel('time (sec)')

Kc_slide = wg.FloatSlider(value=2.0,min=-2.0,max=10.0,step=0.1)
wg.interact(pidPlot, Kc=Kc_slide)
print('P-only Simulator with and without OP Limits: Adjust Kc')