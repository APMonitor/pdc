import numpy as np
%matplotlib inline
import matplotlib.pyplot as plt
from scipy.integrate import odeint
import ipywidgets as wg
from IPython.display import display

n = 1201 # time points to plot
tf = 1200.0 # final time

# TCLab Second-Order
Kp = 0.8473
Kd = 0.3
taus = 51.08
zeta = 1.581
thetap = 0.0

def process(z,t,u):
    x1,y1,x2,y2 = z
    dx1dt = (1.0/(taus**2)) * (-2.0*zeta*taus*x1-(y1-23.0) + Kp*u + Kd*(y2-y1))
    dy1dt = x1
    dx2dt = (1.0/(taus**2)) * (-2.0*zeta*taus*x2-(y2-23.0) + Kd*(y1-y2))
    dy2dt = x2
    return [dx1dt,dy1dt,dx2dt,dy2dt]

def pidPlot(Kc,tauI):
    t = np.linspace(0,tf,n) # create time vector
    P = np.zeros(n)         # initialize proportional term
    I = np.zeros(n)         # initialize integral term 
    e = np.zeros(n)         # initialize error
    ie = np.zeros(n)        # initialize integral error
    OP = np.zeros(n)        # initialize controller output
    PV1 = np.ones(n)*23.0   # initialize process variable
    PV2 = np.ones(n)*23.0   # initialize process variable
    SP2 = np.ones(n)*23.0   # initialize setpoint
    SP2[10:] = 35.0         # step up
    z0 = [0,23.0,0,23.0]    # initial condition
    # loop through all time steps
    for i in range(1,n):
        # simulate process for one time step
        ts = [t[i-1],t[i]]         # time interval
        z = odeint(process,z0,ts,args=(OP[max(0,i-1-int(thetap))],))
        z0 = z[1]                  # record new initial condition
        # calculate new OP with PID
        PV1[i] = z0[1]             # record PV 1
        PV2[i] = z0[3]             # record PV 2
        e[i] = SP2[i] - PV2[i]     # calculate error = SP - PV
        ie[i] = e[i] + ie[i-1]
        dt = t[i] - t[i-1]         # calculate time step
        P[i] = Kc * e[i]           # calculate proportional term
        I[i] = Kc/tauI * ie[i]
        OP[i] = min(100,max(0,P[i]+I[i])) # calculate new controller output        
        if OP[i]==100 or OP[i]==0:
            ie[i] = ie[i-1] # anti-windup

    # plot PID response
    plt.figure(1,figsize=(15,5))
    plt.subplot(1,2,1)
    plt.plot(t,PV1,'r-',linewidth=2,label='Temperature 1')
    plt.plot(t,SP2,'k-',linewidth=2,label='T2 Setpoint (SP)')
    plt.plot(t,PV2,'b--',linewidth=2,label='Temperature 2')
    plt.ylabel(r'T $(^oC)$')
    plt.text(800,30,r'$K_c$: ' + str(np.round(Kc,1)))  
    plt.text(800,26,r'$\tau_I$: ' + str(np.round(tauI,1)))  
    plt.text(800,40,r'IAE: ' + str(np.round(np.sum(np.abs(e)),1)))  
    plt.legend(loc=1)
    plt.xlabel('time (sec)')
    plt.subplot(1,2,2)
    plt.plot(t,OP,'r-',linewidth=2,label='Heater 1 (OP)')
    plt.ylabel('Heater (%)')
    plt.legend(loc='best')
    plt.xlabel('time (sec)')

Kc_slide = wg.FloatSlider(value=2.0,min=1.0,max=10.0,step=1.0)
tauI_slide = wg.FloatSlider(value=150.0,min=5.0,max=300.0,step=5.0)
wg.interact(pidPlot, Kc=Kc_slide, tauI=tauI_slide)
print('PI Control: Adjust Kc and tauI')