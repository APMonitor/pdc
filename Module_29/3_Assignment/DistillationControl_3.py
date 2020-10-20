import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

# define model
def distill(x,t,rr,Feed,x_Feed):
    # Inputs (3):
    # Reflux ratio is the Manipulated variable
    # Reflux Ratio (L/D)
    #rr = p(1)

    # Disturbance variables (DV)
    # Feed Flowrate (mol/min)
    #Feed = p(2)

    # Mole Fraction of Feed
    #x_Feed = p(3)

    # States (32):
    # x(0) - Reflux Drum Liquid Mole Fraction of Component A
    # x(1) - Tray 1 - Liquid Mole Fraction of Component A
    # .
    # .
    # .
    # x(16) - Tray 16 - Liquid Mole Fraction of Component A (Feed)
    # .
    # .
    # .
    # x(30) - Tray 30 - Liquid Mole Fraction of Component A
    # x(31) - Reboiler Liquid Mole Fraction of Component A

    # Parameters
    # Distillate Flowrate (mol/min)
    D=0.5*Feed
    # Flowrate of the Liquid in the Rectification Section (mol/min)
    L=rr*D
    # Vapor Flowrate in the Column (mol/min)
    V=L+D
    # Flowrate of the Liquid in the Stripping Section (mol/min)
    FL=Feed+L
    # Relative Volatility = (yA/xA)/(yB/xB) = KA/KB = alpha(A,B)
    vol=1.6
    # Total Molar Holdup in the Condenser
    atray=0.25
    # Total Molar Holdup on each Tray
    acond=0.5
    # Total Molar Holdup in the Reboiler
    areb=1.0
    # Vapor Mole Fractions of Component A
    # From the equilibrium assumption and mole balances
    # 1) vol = (yA/xA) / (yB/xB)
    # 2) xA + xB = 1
    # 3) yA + yB = 1
    y = np.empty(len(x))
    for i in range(32):
        y[i] = x[i] * vol/(1.0+(vol-1.0)*x[i])

    # Compute xdot
    xdot = np.empty(len(x))
    xdot[0] = 1/acond*V*(y[1]-x[0])
    for i in range(1,16):
        xdot[i] = 1.0/atray*(L*(x[i-1]-x[i])-V*(y[i]-y[i+1]))
    xdot[16] = 1/atray*(Feed*x_Feed+L*x[15]-FL*x[16]-V*(y[16]-y[17]))
    for i in range(17,31):
        xdot[i] = 1.0/atray*(FL*(x[i-1]-x[i])-V*(y[i]-y[i+1]))
    xdot[31] = 1/areb*(FL*x[30]-(Feed-D)*x[31]-V*y[31])
    return xdot

# Steady State Initial Conditions for the 32 states
x_ss =np.array([0.935,0.900,0.862,0.821,0.779,0.738,\
0.698,0.661,0.628,0.599,0.574,0.553,0.535,0.521,    \
0.510,0.501,0.494,0.485,0.474,0.459,0.441,0.419,    \
0.392,0.360,0.324,0.284,0.243,0.201,0.161,0.125,    \
0.092,0.064])
x0 = x_ss

# Steady State Initial Condition
rr_ss = 3.0

# Time Interval (min)
ns = 101
t = np.linspace(0,100,ns)

# Store results for plotting
xd = np.ones(len(t)) * x_ss[0]
rr = np.ones(len(t)) * rr_ss
ff = np.ones(len(t))
xf = np.ones(len(t)) * 0.5

# Step in reflux ratio
#rr[10:] = 4.0
#rr[40:] = 2.0
#rr[70:] = 3.0

# Feed Concentration (mol frac)
xf[50:] = 0.42

# Feed flow rate
#ff[80:] = 1.0

delta_t = t[1]-t[0]

# storage for recording values
op = np.ones(ns)*3.0  # controller output
pv = np.zeros(ns)  # process variable
e = np.zeros(ns)   # error
ie = np.zeros(ns)  # integral of the error
dpv = np.zeros(ns) # derivative of the pv
P = np.zeros(ns)   # proportional
I = np.zeros(ns)   # integral
D = np.zeros(ns)   # derivative
sp = np.ones(ns)*0.935  # set point
sp[10:] = 0.97

# PID (tuning)
Kc = 60
tauI = 4
tauD = 0.0

# Upper and Lower limits on OP
op_hi = 10.0
op_lo = 1.0

# loop through time steps    
for i in range(1,ns):
    e[i] = sp[i] - pv[i]
    if i >= 1:  # calculate starting on second cycle
        dpv[i] = (pv[i]-pv[i-1])/delta_t
        ie[i] = ie[i-1] + e[i] * delta_t
    P[i] = Kc * e[i]
    I[i] = Kc/tauI * ie[i]
    D[i] = - Kc * tauD * dpv[i]
    op[i] = op[0] + P[i] + I[i] + D[i]
    if op[i] > op_hi:  # check upper limit
        op[i] = op_hi
        ie[i] = ie[i] - e[i] * delta_t # anti-reset windup
    if op[i] < op_lo:  # check lower limit
        op[i] = op_lo
        ie[i] = ie[i] - e[i] * delta_t # anti-reset windup

    # distillation solution (1 time step)
    rr[i] = op[i]
    ts = [t[i-1],t[i]]
    y = odeint(distill,x0,ts,args=(rr[i],ff[i],xf[i]))
    xd[i] = y[-1][0]
    x0 = y[-1]

    if i<ns-1:
        pv[i+1] = y[-1][0]

#op[ns] = op[ns-1]
#ie[ns] = ie[ns-1]
#P[ns] = P[ns-1]
#I[ns] = I[ns-1]
#D[ns] = D[ns-1]    


# Construct results and save data file
# Column 1 = time
# Column 2 = reflux ratio
# Column 3 = distillate composition
data = np.vstack((t,rr,xd)) # vertical stack
data = data.T             # transpose data
np.savetxt('data.txt',data,delimiter=',')

# Plot the results
plt.figure()
plt.subplot(3,1,1)
plt.plot(t,rr,'b--',linewidth=3)
plt.ylabel(r'$RR$')
plt.legend(['Reflux ratio'],loc='best')

plt.subplot(3,1,2)
plt.plot(t,xf,'k:',linewidth=3,label='Feed composition')
plt.plot(t,ff,'g-.',linewidth=3,label='Feed flow (mol/min)')
plt.ylabel('Feed')
plt.ylim([0.4,1.1])
plt.legend(loc='best')

plt.subplot(3,1,3)
plt.plot(t,xd,'r-',linewidth=3)
plt.plot(t,sp,'k.-',linewidth=1)
plt.ylabel(r'$x_d\;(mol/L)$')
plt.legend(['Distillate composition','Set point'],loc='best')
plt.xlabel('Time (min)')
plt.savefig('distillation.png')
plt.show()