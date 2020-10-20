import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

# specify number of steps
ns = 1200
# define time points
t = np.linspace(0,ns,ns+1)

# mode (manual=0, automatic=1)
mode = 1

class model(object):
    # process model
    Kp = 2.0
    taup = 200.0
    thetap = 0.0

class pid(object):
    # PID tuning
    Kc = 2.0
    tauI = 10.0
    tauD = 0
    sp = []

# Define Set Point
sp = np.zeros(ns+1)  # set point
sp[50:600] = 10
sp[600:] = 0
pid.sp = sp

def process(y,t,u,Kp,taup):
    # Kp = process gain
    # taup = process time constant
    dydt = -y/taup + Kp/taup * u
    return dydt

def calc_response(t,mode,xm,xc):
    # t = time points
    # mode (manual=0, automatic=1)
    # process model
    Kp = xm.Kp
    taup = xm.taup
    thetap = xm.thetap
    # specify number of steps
    ns = len(t)-1
    # PID tuning
    Kc = xc.Kc
    tauI = xc.tauI
    tauD = xc.tauD
    sp = xc.sp  # set point

    delta_t = t[1]-t[0]

    # storage for recording values
    op = np.zeros(ns+1)  # controller output
    pv = np.zeros(ns+1)  # process variable
    e = np.zeros(ns+1)   # error
    ie = np.zeros(ns+1)  # integral of the error
    dpv = np.zeros(ns+1) # derivative of the pv
    P = np.zeros(ns+1)   # proportional
    I = np.zeros(ns+1)   # integral
    D = np.zeros(ns+1)   # derivative

    # step input for manual control
    if mode==0:
        op[100:]=2

    # Upper and Lower limits on OP
    op_hi = 100.0
    op_lo = 0.0

    # Simulate time delay
    ndelay = int(np.ceil(thetap / delta_t)) 

    # loop through time steps    
    for i in range(0,ns):
        e[i] = sp[i] - pv[i]
        if i >= 1:  # calculate starting on second cycle
            dpv[i] = (pv[i]-pv[i-1])/delta_t
            ie[i] = ie[i-1] + e[i] * delta_t
        P[i] = Kc * e[i]
        I[i] = Kc/tauI * ie[i]
        D[i] = - Kc * tauD * dpv[i]
        if mode==1:
            op[i] = op[0] + P[i] + I[i] + D[i]
        if op[i] > op_hi:  # check upper limit
            op[i] = op_hi
            ie[i] = ie[i] - e[i] * delta_t # anti-reset windup
        if op[i] < op_lo:  # check lower limit
            op[i] = op_lo
            ie[i] = ie[i] - e[i] * delta_t # anti-reset windup
        # implement time delay
        iop = max(0,i-ndelay)
        y = odeint(process,pv[i],[0,delta_t],args=(op[iop],Kp,taup))
        pv[i+1] = y[-1]
    op[ns] = op[ns-1]
    ie[ns] = ie[ns-1]
    P[ns] = P[ns-1]
    I[ns] = I[ns-1]
    D[ns] = D[ns-1]
    return (pv,op) 

def plot_response(n,mode,t,pv,op,sp):
    # plot results
    plt.figure(n)

    plt.subplot(2,1,1)
    if (mode==1):
        plt.plot(t,sp,'k-',linewidth=2,label='Set Point (SP)')
    plt.plot(t,pv,'b--',linewidth=3,label='Process Variable (PV)')
    plt.legend(loc='best')
    plt.ylabel('Process Output')

    plt.subplot(2,1,2)
    plt.plot(t,op,'r:',linewidth=3,label='Controller Output (OP)')
    plt.legend(loc='best')
    plt.ylabel('Process Input')

    plt.xlabel('Time')

# calculate step response
model.Kp = 2.0
model.taup = 200.0
model.thetap = 0.0
mode = 0
(pv,op) = calc_response(t,mode,model,pid)
plot_response(1,mode,t,pv,op,sp)

# PI control
pid.Kc = 2.0
pid.tauI = 10.0
pid.tauD = 0.0
mode = 1
(pv,op) = calc_response(t,mode,model,pid)
plot_response(2,mode,t,pv,op,sp)

plt.show()