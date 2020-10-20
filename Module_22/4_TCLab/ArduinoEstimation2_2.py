import numpy as np
import pandas as pd
%matplotlib inline
import matplotlib.pyplot as plt
from scipy.integrate import odeint
import ipywidgets as wg
from IPython.display import display

# try to read local data file first
try:
    filename = 'data.csv'
    data = pd.read_csv(filename)
except:
    filename = 'http://apmonitor.com/pdc/uploads/Main/tclab_data2.txt'
    data = pd.read_csv(filename)

n = 601 # time points to plot
tf = 600.0 # final time

# Use expected room temperature for initial condition
#y0 = [23.0,23.0]
# Use initial condition
y0d = [data['T1'].values[0],data['T2'].values[0]]

# load data
Q1 = data['Q1'].values
Q2 = data['Q2'].values
T1 = data['T1'].values
T2 = data['T2'].values
T1p = np.ones(n)*y0d[0]
T2p = np.ones(n)*y0d[1]

def process(y,t,u1,u2,Kp,Kd,taup):
    y1,y2 = y
    dy1dt = (1.0/taup) * (-(y1-y0d[0]) + Kp * u1 + Kd * (y2-y1))
    dy2dt = (1.0/taup) * (-(y2-y0d[1]) + (Kp/2.0) * u2 + Kd * (y1-y2))
    return [dy1dt,dy2dt]

def fopdtPlot(Kp,Kd,taup,thetap):
    y0 = y0d
    t = np.linspace(0,tf,n) # create time vector
    iae = 0.0
    # loop through all time steps
    for i in range(1,n):
        # simulate process for one time step
        ts = [t[i-1],t[i]]         # time interval
        inputs = (Q1[max(0,i-int(thetap))],Q2[max(0,i-int(thetap))],Kp,Kd,taup)
        y = odeint(process,y0,ts,args=inputs)
        y0 = y[1]                  # record new initial condition
        T1p[i] = y0[0]
        T2p[i] = y0[1]        
        iae += np.abs(T1[i]-T1p[i]) + np.abs(T2[i]-T2p[i])

    # plot FOPDT response
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
    plt.text(400,25,r'$\tau_p$: ' + str(np.round(taup,0)) + ' sec')  
    plt.text(400,20,r'$\theta_p$: ' + str(np.round(thetap,0)) + ' sec')  
    plt.legend(loc=2)
    plt.subplot(2,1,2)
    plt.plot(t,Q1,'b--',linewidth=2,label=r'Heater 1 ($Q_1$)')
    plt.plot(t,Q2,'r:',linewidth=2,label=r'Heater 2 ($Q_2$)')
    plt.legend(loc='best')
    plt.xlabel('time (sec)')

Kp_slide = wg.FloatSlider(value=0.5,min=0.1,max=1.5,step=0.05)
Kd_slide = wg.FloatSlider(value=0.0,min=0.0,max=1.0,step=0.05)
taup_slide = wg.FloatSlider(value=50.0,min=50.0,max=250.0,step=5.0)
thetap_slide = wg.FloatSlider(value=0,min=0,max=30,step=1)
wg.interact(fopdtPlot, Kp=Kp_slide, Kd=Kd_slide, taup=taup_slide,thetap=thetap_slide)
print('FOPDT Simulator: Adjust Kp, Kd, taup, and thetap ' + \
      'to achieve lowest Integral Abs Error')