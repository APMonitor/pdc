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
t = np.linspace(0,10,100)

# Store results for plotting
xd = np.ones(len(t)) * x_ss[0]
rr = np.ones(len(t)) * rr_ss
ff = np.ones(len(t))
xf = np.ones(len(t)) * 0.5
sp = np.ones(len(t)) * 0.97

# Step in reflux ratio
rr[10:] = 3.5

# Feed Concentration (mol frac)
xf[50:] = 0.42

# Feed flow rate
ff[80:] = 1.0

plt.figure(figsize=(10,7))
plt.ion()
plt.show()

# Simulate
for i in range(len(t)-1):
    ts = [t[i],t[i+1]]
    y = odeint(distill,x0,ts,args=(rr[i],ff[i],xf[i]))
    xd[i+1] = y[-1][0]
    x0 = y[-1]

    # Plot the results
    plt.clf()
    plt.subplot(3,1,1)
    plt.plot(t[0:i+1],rr[0:i+1],'b--',linewidth=3)
    plt.ylabel(r'$RR$')
    plt.legend(['Reflux ratio'],loc='best')

    plt.subplot(3,1,2)
    plt.plot(t[0:i+1],xf[0:i+1],'k:',linewidth=3,label='Feed composition')
    plt.plot(t[0:i+1],ff[0:i+1],'g-.',linewidth=3,label='Feed flow (mol/min)')
    plt.ylabel('Feed')
    plt.ylim([0.4,1.1])
    plt.legend(loc='best')

    plt.subplot(3,1,3)
    plt.plot(t[0:i+1],xd[0:i+1],'r-',linewidth=3)
    plt.plot(t[0:i+1],sp[0:i+1],'k.-',linewidth=1)
    plt.ylabel(r'$x_d\;(mol/L)$')
    plt.legend(['Distillate composition','Set point'],loc='best')
    plt.xlabel('Time (min)')

    plt.draw()
    plt.pause(0.05)

# Construct results and save data file
# Column 1 = time
# Column 2 = reflux ratio
# Column 3 = distillate composition
data = np.vstack((t,rr,xd)) # vertical stack
data = data.T             # transpose data
np.savetxt('data.txt',data,delimiter=',')

plt.savefig('distillation.png')