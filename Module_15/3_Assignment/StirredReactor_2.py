
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from simple_pid import PID  # pip install simple_pid
import time

make_gif = True
try:
    import imageio  # required to make gif animation
except:
    print('install imageio with "pip install imageio" to make gif')
    make_gif=False
if make_gif:
    try:
        import os
        images = []
        os.mkdir('./frames')
    except:
        pass

# define CSTR model
def cstr(x,t,u,Tf,Caf):
    # Inputs (3):
    # Temperature of cooling jacket (K)
    Tc = u
    # Tf = Feed Temperature (K)
    # Caf = Feed Concentration (mol/m^3)

    # States (2):
    # Concentration of A in CSTR (mol/m^3)
    Ca = x[0]
    # Temperature in CSTR (K)
    T = x[1]

    # Parameters:
    # Volumetric Flowrate (m^3/sec)
    q = 100
    # Volume of CSTR (m^3)
    V = 100
    # Density of A-B Mixture (kg/m^3)
    rho = 1000
    # Heat capacity of A-B Mixture (J/kg-K)
    Cp = 0.239
    # Heat of reaction for A->B (J/mol)
    mdelH = 5e4
    # E - Activation energy in the Arrhenius Equation (J/mol)
    # R - Universal Gas Constant = 8.31451 J/mol-K
    EoverR = 8750
    # Pre-exponential factor (1/sec)
    k0 = 7.2e10
    # U - Overall Heat Transfer Coefficient (W/m^2-K)
    # A - Area - this value is specific for the U calculation (m^2)
    UA = 5e4
    # reaction rate
    rA = k0*np.exp(-EoverR/T)*Ca

    # Calculate concentration derivative
    dCadt = q/V*(Caf - Ca) - rA
    # Calculate temperature derivative
    dTdt = q/V*(Tf - T) \
            + mdelH/(rho*Cp)*rA \
            + UA/V/rho/Cp*(Tc-T)

    # Return xdot:
    xdot = np.zeros(2)
    xdot[0] = dCadt
    xdot[1] = dTdt
    return xdot

# Steady State Initial Conditions for the States
Ca_ss = 0.87725294608097
T_ss = 324.475443431599
x0 = np.empty(2)
x0[0] = Ca_ss
x0[1] = T_ss

# Steady State Initial Condition
u_ss = 300.0
# Feed Temperature (K)
Tf = 350
# Feed Concentration (mol/m^3)
Caf = 1

# Time Interval (min)
t = np.linspace(0,10,101)

# Store results for plotting
Ca = np.ones(len(t)) * Ca_ss
T = np.ones(len(t)) * T_ss
u = np.ones(len(t)) * u_ss

# setpoint
sp = np.ones(101) * T_ss
sp[5:] = 340.0
u_bias = u_ss

# create PID controller
# op = op_bias + Kc * e + Ki * ei + Kd * ed
#      with ei = error integral
#      with ed = error derivative
Kc = 1.0      # Controller gain
Ki = 1.0      # Controller integral parameter
Kd = 0.0      # Controller derivative parameter
pid = PID(Kc,Ki,Kd)
# lower and upper controller output limits
oplo = 250.0
ophi = 350.0
pid.output_limits = (oplo-u_bias,ophi-u_bias)
# PID sample time
pid.sample_time = 0.1

plt.figure(1)
plt.ion()
plt.show()

# timing functions
tm = np.zeros(101)
sleep_max = 0.101
start_time = time.time()
prev_time = start_time

# Simulate CSTR
for i in range(len(t)-1):
    # PID control
    pid.setpoint=sp[i]
    u[i+1] = pid(T[i]) + u_bias

    ts = [t[i],t[i+1]]
    y = odeint(cstr,x0,ts,args=(u[i+1],Tf,Caf))
    Ca[i+1] = y[-1][0]
    T[i+1] = y[-1][1]
    x0[0] = Ca[i+1]
    x0[1] = T[i+1]

    # plot results
    plt.clf()
    # Plot the results
    plt.subplot(3,1,1)
    plt.plot(t[0:i+1],u[0:i+1],'b--',linewidth=3)
    plt.ylabel('Cooling T (K)')
    plt.legend(['Jacket Temperature'],loc='best')

    plt.subplot(3,1,2)
    plt.plot(t[0:i+1],Ca[0:i+1],'r-',linewidth=3)
    plt.ylabel('Ca (mol/L)')
    plt.legend(['Reactor Concentration'],loc='best')

    plt.subplot(3,1,3)
    plt.plot([t[0],t[i]],[400.0,400.0],'r-',linewidth=2)
    plt.plot(t[0:i+1],T[0:i+1],'b.-',linewidth=3)
    plt.plot(t[0:i+1],sp[0:i+1],'k:',linewidth=3)
    plt.ylabel('T (K)')
    plt.xlabel('Time (min)')
    plt.legend(['Upper Limit','Reactor Temperature','Set Point'],loc='best')
    plt.pause(0.001)

    if make_gif:
        filename='./frames/frame_'+str(1000+i)+'.png'
        plt.savefig(filename)
        images.append(imageio.imread(filename))

    # Sleep time
    sleep = sleep_max - (time.time() - prev_time)
    if sleep>=0.001:
        time.sleep(sleep-0.001)
    else:
        time.sleep(0.001)

    # Record time and change in time
    ct = time.time()
    dt = ct - prev_time
    prev_time = ct
    tm[i+1] = ct - start_time



# Construct results and save data file
# Column 1 = time
# Column 2 = cooling temperature
# Column 3 = reactor temperature
data = np.vstack((t,u,T)) # vertical stack
data = data.T             # transpose data
np.savetxt('data.txt',data,delimiter=',')

# create animated GIF
if make_gif:
    imageio.mimsave('animate.gif', images)
    #imageio.mimsave('animate.mp4', images)  # requires ffmpeg