import tclab
import numpy as np
import time
import matplotlib.pyplot as plt
from gekko import GEKKO
import random

# Detect session is IPython
try:
    from IPython import get_ipython
    from IPython.display import display,clear_output
    get_ipython().run_line_magic('matplotlib', 'inline')
    ipython = True
    print('IPython Notebook')
except:
    ipython = False
    print('Not IPython Notebook')

# magnitude of step
M = 80

# 2nd order step response
def model(T0,t,M,Kp,taus,zeta):
    # T0 = initial T
    # t  = time
    # M  = magnitude of the step
    # Kp = gain
    # taus = second order time constant
    # zeta = damping factor (zeta>1 for overdamped)
    T = ?
    return T

# Connect to Arduino
a = tclab.TCLab()

# Second order model of TCLab
m = GEKKO(remote=False)
Kp   = m.FV(1.0,lb=0.5,ub=2.0)
taus = m.FV(50,lb=10,ub=200)
zeta =  m.FV(1.2,lb=1.1,ub=5)
y0 = a.T1
u = m.MV(0)
x = m.Var(y0); y = m.CV(y0)
m.Equation(x==y.dt())
m.Equation((taus**2)*x.dt()+2*zeta*taus*y.dt()+(y-y0) == Kp*u)
m.options.IMODE = 5
m.options.NODES = 2
m.time = np.linspace(0,200,101)
m.solve(disp=False)
y.FSTATUS = 1

# Turn LED on
print('LED On')
a.LED(100)

# Run time in minutes
run_time = 5

# Number of cycles
loops = int(30.0*run_time)
tm = np.zeros(loops)
z = np.zeros(loops)

# Temperature (K)
T1 = np.ones(loops) * a.T1 # measured T (degC)
T1p = np.ones(loops) * a.T1 # predicted T (degC)

# step test (0 - 100%)
Q1 = np.ones(loops) * 0.0
Q1[1:] = M # magnitude of the step

print('Running Main Loop. Ctrl-C to end.')
print('  Time   Kp    taus    zeta')

# Create plot
if not ipython:
    plt.figure(figsize=(10,7))
    plt.ion()
    plt.show()

# Main Loop
start_time = time.time()
prev_time = start_time
try:
    for i in range(1,loops):
        # Sleep time
        sleep_max = 2.0
        sleep = sleep_max - (time.time() - prev_time)
        if sleep>=0.01:
            time.sleep(sleep)
        else:
            time.sleep(0.01)

        # Record time and change in time
        t = time.time()
        dt = t - prev_time
        prev_time = t
        tm[i] = t - start_time

        # Read temperatures in Kelvin 
        T1[i] = a.T1

        # Regression with Gekko
        if i==5:
            Kp.STATUS = 1
            taus.STATUS = 1
            zeta.STATUS = 1
        u.meas = Q1[i]
        y.meas = T1[i]
        m.solve(disp=False)

        # Update 2nd order prediction
        Kpm = Kp.value[0]; tausm = taus.value[0]; zetam = zeta.value[0]
        for j in range(1,i+1):
            T1p[j] = model(T1p[0],tm[j],M,Kpm,tausm,zetam)

        # Write output (0-100)
        a.Q1(Q1[i])

        # Print line of data
        if np.mod(i,15)==0:
            print('  Time   Kp    taus    zeta')
        print('{:6.1f} {:6.2f} {:6.2f} {:6.2f}'\
              .format(tm[i],Kpm,tausm,zetam))

        # Plot
        if ipython:
            plt.figure(figsize=(10,7))
        else:
            plt.clf()
        ax=plt.subplot(2,1,1)
        ax.grid()
        plt.plot(tm[0:i],T1[0:i],'ro',label=r'$T_1 \, Meas$')
        plt.plot(tm[0:i],T1p[0:i],'k-',label=r'$T_1 \, Pred$')
        plt.ylabel('Temperature (degC)')
        plt.legend(loc=2)
        ax=plt.subplot(2,1,2)
        ax.grid()
        plt.plot(tm[0:i],Q1[0:i],'b-',label=r'$Q_1$')
        plt.ylabel('Heaters')
        plt.xlabel('Time (sec)')
        plt.legend(loc='best')
        if ipython:
            clear_output(wait=True)
            display(plt.gcf())
        else:
            plt.draw()
            plt.pause(0.05)

    # Turn off heaters
    a.Q1(0)
    a.Q2(0)
    a.close()
    # Save figure
    plt.savefig('test_Second_Order.png')

# Allow user to end loop with Ctrl-C           
except KeyboardInterrupt:
    # Disconnect from Arduino
    a.Q1(0)
    a.Q2(0)
    print('Shutting down')
    a.close()
    plt.savefig('test_Second_Order.png')

# Make sure serial connection still closes when there's an error
except:           
    # Disconnect from Arduino
    a.Q1(0)
    a.Q2(0)
    print('Error: Shutting down')
    a.close()
    plt.savefig('test_Second_Order.png')
    raise