import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

# animate plots?
animate=True # True / False

def tank(levels,t,pump,valve):
    h1 = max(0.0,levels[0])
    h2 = max(0.0,levels[1])
    c1 = 0.08 # inlet valve coefficient
    c2 = 0.04 # tank outlet coefficient
    dhdt1 = c1 * (1.0-valve) * pump - c2 * np.sqrt(h1)
    dhdt2 = c1 * valve * pump + c2 * np.sqrt(h1) - c2 * np.sqrt(h2)
    # overflow conditions
    if h1>=1.0 and dhdt1>0.0:
        dhdt1 = 0
    if h2>=1.0 and dhdt2>0.0:
        dhdt2 = 0
    dhdt = [dhdt1,dhdt2]
    return dhdt

# Initial conditions (levels)
h0 = [0.0,0.0]

# Time points to report the solution
tf = 200
t = np.linspace(0,tf,tf+1)
# Inputs that can be adjusted
pump = np.zeros((tf+1))
# pump can operate between 0 and 1
pump[10:] = 0.2
# valve = 0, directly into top tank
# valve = 1, directly into bottom tank
valve = 0.0 
# Record the solution
y = np.empty((tf+1,2))
y[0,:] = h0

plt.figure(1)

if animate:
    plt.ion()
    plt.show()

# Simulate the tank step test
for i in range(tf):
    # Specify the pump and valve
    inputs = (pump[i],valve)
    # Integrate the model
    h = odeint(tank,h0,[0,1],inputs)
    # Record the result
    y[i+1,:] = h[-1,:]
    # Reset the initial condition
    h0 = h[-1,:]

    # plot results
    if animate:
        plt.clf()    
        plt.subplot(2,1,1)
        plt.plot(t[0:i+1],y[0:i+1,0],'b-',label='height 1')
        plt.plot(t[0:i+1],y[0:i+1,1],'r--',label='height 2')
        plt.ylabel('Height (m)')
        plt.legend(loc='best')
        plt.subplot(2,1,2)
        plt.plot(t[0:i+1],pump[0:i+1],'k-',label='pump')
        plt.legend(loc='best')
        plt.ylabel('Pump')
        plt.xlabel('Time (sec)')
        plt.pause(0.01)

# Export step test data file
# reshape as column vectors
time_col = t.reshape(-1,1)
pump_col = pump.reshape(-1,1)
h2_col = y[:,1].reshape(-1,1)
my_data = np.concatenate((time_col,pump_col,h2_col), axis=1)
np.savetxt('step_test_data.txt',my_data,delimiter=',')

if not animate:
    # Plot results
    plt.subplot(2,1,1)
    plt.plot(t,y[:,0],'b-',label='height 1')
    plt.plot(t,y[:,1],'r--',label='height 2')
    plt.ylabel('Height (m)')
    plt.legend(loc='best')
    plt.subplot(2,1,2)
    plt.plot(t,pump,'k-',label='pump')
    plt.legend(loc='best')
    plt.ylabel('Pump')
    plt.xlabel('Time (sec)')
    plt.show()