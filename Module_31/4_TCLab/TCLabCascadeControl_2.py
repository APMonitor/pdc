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

def pidPlot(Kc1,tauI1,Kc2,tauI2):
    t = np.linspace(0,tf,n) # create time vector
    P1 = np.zeros(n)         # initialize proportional term
    I1 = np.zeros(n)         # initialize integral term 
    P2 = np.zeros(n)         # initialize proportional term
    I2 = np.zeros(n)         # initialize integral term 
    e1 = np.zeros(n)         # initialize error
    ie1 = np.zeros(n)        # initialize integral error
    e2 = np.zeros(n)         # initialize error
    ie2 = np.zeros(n)        # initialize integral error
    OP = np.zeros(n)        # initialize controller output
    PV1 = np.ones(n)*23.0   # initialize process variable
    PV2 = np.ones(n)*23.0   # initialize process variable
    SP1 = np.ones(n)*23.0   # initialize setpoint
    SP2 = np.ones(n)*23.0   # initialize setpoint
    SP2[10:] = 35.0         # step up
    z0 = [0,23.0,0,23.0]    # initial condition
    iae = 0.0
    # loop through all time steps
    for i in range(1,n):
        # simulate process for one time step
        ts = [t[i-1],t[i]]         # time interval
        z = odeint(process,z0,ts,args=(OP[max(0,i-1-int(thetap))],))
        z0 = z[1]                  # record new initial condition
        dt = t[i] - t[i-1]         # calculate time step

        # outer loop
        PV2[i] = z0[3]             # record PV 2
        e2[i] = SP2[i] - PV2[i]     # calculate error = SP - PV
        ie2[i] = e2[i]*dt + ie2[i-1]
        P2[i] = Kc2 * e2[i]    # calculate proportional term
        I2[i] = Kc2/tauI2 * ie2[i]
        SP1[i] = min(85,max(23,P2[i]+I2[i])) # calculate new controller output        
        if SP1[i]==85 or SP1[i]==23:
            ie2[i] = ie2[i-1] # anti-windup

        # inner loop
        PV1[i] = z0[1]             # record PV 1
        e1[i] = SP1[i] - PV1[i]     # calculate error = SP - PV
        ie1[i] = e1[i]*dt + ie1[i-1]
        P1[i] = Kc1 * e1[i]           # calculate proportional term
        I1[i] = Kc1/tauI1 * ie1[i]
        OP[i] = min(100,max(0,P1[i]+I1[i])) # calculate new controller output        
        if OP[i]==100 or OP[i]==0:
            ie1[i] = ie1[i-1] # anti-windup

    # plot PID response
    plt.figure(1,figsize=(15,5))
    plt.subplot(1,2,1)
    plt.plot(t,SP1,'k:',linewidth=2,label='T1 Setpoint (SP)')
    plt.plot(t,PV1,'r-',linewidth=2,label='Temperature 1')
    plt.plot(t,SP2,'k-',linewidth=2,label='T2 Setpoint (SP)')
    plt.plot(t,PV2,'b--',linewidth=2,label='Temperature 2')
    plt.ylabel(r'T $(^oC)$')
    plt.text(500,30,'Inner Loop 1')  
    plt.text(500,26,r'$K_{c1}$: ' + str(np.round(Kc1,1)))  
    plt.text(500,22,r'$\tau_{I1}$: ' + str(np.round(tauI1,1)))  
    plt.text(800,30,'Outer Loop 2')  
    plt.text(800,26,r'$K_{c2}$: ' + str(np.round(Kc2,1)))  
    plt.text(800,22,r'$\tau_{I2}$: ' + str(np.round(tauI2,1))) 
    plt.text(800,40,r'IAE: ' + str(np.round(np.sum(np.abs(e2)),1)))  
    plt.legend(loc=1)
    plt.xlabel('time (sec)')
    plt.subplot(1,2,2)
    plt.plot(t,OP,'r-',linewidth=2,label='Heater 1 (OP)')
    plt.ylabel('Heater (%)')
    plt.legend(loc='best')
    plt.xlabel('time (sec)')

Kc1_slide = wg.FloatSlider(value=2.0,min=1.0,max=10.0,step=0.5)
tauI1_slide = wg.FloatSlider(value=200.0,min=5.0,max=300.0,step=5.0)
Kc2_slide = wg.FloatSlider(value=3.0,min=2.0,max=10.0,step=0.5)
tauI2_slide = wg.FloatSlider(value=150.0,min=5.0,max=300.0,step=5.0)
wg.interact(pidPlot, Kc1=Kc1_slide, tauI1=tauI1_slide, \
            Kc2=Kc2_slide, tauI2=tauI2_slide)
print('PI Cascade Control: Adjust Kc1, Kc2, tauI1, tauI2')