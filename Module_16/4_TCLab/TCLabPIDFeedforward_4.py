import tclab
import numpy as np
import time
import matplotlib.pyplot as plt
from scipy.integrate import odeint

#-----------------------------------------
# PID controller performance for the TCLab
#-----------------------------------------
# PID Parameters
Kc   = 5.0
tauI = 120.0 # sec
tauD = 2.0   # sec
Kff  = 

#-----------------------------------------
# PID Controller with Feedforward
#-----------------------------------------
# inputs ---------------------------------
# sp = setpoint
# pv = current temperature
# pv_last = prior temperature
# ierr = integral error
# dt = time increment between measurements
# outputs --------------------------------
# op = output of the PID controller
# P = proportional contribution
# I = integral contribution
# D = derivative contribution
def pid(sp,pv,pv_last,ierr,dt,d):
    # Parameters in terms of PID coefficients
    KP = Kc
    KI = Kc/tauI
    KD = Kc*tauD
    # ubias for controller (initial heater)
    op0 = 0 
    # upper and lower bounds on heater level
    ophi = 100
    oplo = 0
    # calculate the error
    error = sp-pv
    # calculate the integral error
    ierr = ierr + KI * error * dt
    # calculate the measurement derivative
    dpv = (pv - pv_last) / dt
    # calculate the PID output
    P = KP * error
    I = ierr
    D = -KD * dpv
    FF = Kff * d
    op = op0 + P + I + D + FF
    # implement anti-reset windup
    if op < oplo or op > ophi:
        I = I - KI * error * dt
        # clip output
        op = max(oplo,min(ophi,op))
    # return the controller output and PID terms
    return [op,P,I,D,FF]

# save txt file with data and set point
# t = time
# u1,u2 = heaters
# y1,y2 = tempeatures
# sp1,sp2 = setpoints
def save_txt(t, u1, u2, y1, y2, sp1, sp2):
    data = np.vstack((t, u1, u2, y1, y2, sp1, sp2))  # vertical stack
    data = data.T  # transpose data
    top = ('Time,Q1,Q2,T1,T2,TSP1,TSP2')
    np.savetxt('validate.txt', data, delimiter=',',\
               header=top, comments='')

# Connect to Arduino
a = tclab.TCLab()

# Turn LED on
print('LED On')
a.LED(100)

# Run time in minutes
run_time = 10.0

# Number of cycles
loops = int(60.0*run_time)
tm = np.zeros(loops)

# Temperature
# set point (degC)
Tsp1 = np.ones(loops) * a.T1

# Heater set point steps
Tsp1[10:] = 40.0

T1 = np.ones(loops) * a.T1 # measured T (degC)
error_sp = np.zeros(loops)

Tsp2 = np.ones(loops) * a.T2 # set point (degC)
T2 = np.ones(loops) * a.T2 # measured T (degC)

# impulse tests (0 - 100%)
Q1 = np.ones(loops) * 0.0
Q2 = np.ones(loops) * 0.0
Q2[200:401] = 100.0

print('Running Main Loop. Ctrl-C to end.')
print('  Time     SP     PV     Q1   =  P   +  I  +   D   + FF   IAE')
print(('{:6.1f} {:6.2f} {:6.2f} ' + \
       '{:6.2f} {:6.2f} {:6.2f} {:6.2f} {:6.2f} {:6.2f}').format( \
           tm[0],Tsp1[0],T1[0], \
           Q1[0],0.0,0.0,0.0,0.0,0.0))

# Main Loop
start_time = time.time()
prev_time = start_time
dt_error = 0.0
# Integral error
ierr = 0.0
# Integral absolute error
iae = 0.0

plt.figure(figsize=(10,7))
plt.ion()
plt.show()

try:
    for i in range(1,loops):
        # Sleep time
        sleep_max = 1.0
        sleep = sleep_max - (time.time() - prev_time) - dt_error
        if sleep>=1e-4:
            time.sleep(sleep-1e-4)
        else:
            print('exceeded max cycle time by ' + str(abs(sleep)) + ' sec')
            time.sleep(1e-4)

        # Record time and change in time
        t = time.time()
        dt = t - prev_time
        if (sleep>=1e-4):
            dt_error = dt-1.0+0.009
        else:
            dt_error = 0.0
        prev_time = t
        tm[i] = t - start_time

        # Read temperatures in Kelvin 
        T1[i] = a.T1
        T2[i] = a.T2

        # Disturbance
        d = T2[i] - 23.0

        # Integral absolute error
        iae += np.abs(Tsp1[i]-T1[i])

        # Calculate PID output
        [Q1[i],P,ierr,D,FF] = pid(Tsp1[i],T1[i],T1[i-1],ierr,dt,d)

        # Write output (0-100)
        a.Q1(Q1[i])
        a.Q2(Q2[i])

        # Print line of data
        print(('{:6.1f} {:6.2f} {:6.2f} ' + \
              '{:6.2f} {:6.2f} {:6.2f} {:6.2f} {:6.2f} {:6.2f}').format( \
                  tm[i],Tsp1[i],T1[i], \
                  Q1[i],P,ierr,D,FF,iae))

        # Update plot
        plt.clf()
        # Plot
        ax=plt.subplot(2,1,1)
        ax.grid()
        plt.plot(tm[0:i],Tsp1[0:i],'k--',label=r'$T_1$ set point')
        plt.plot(tm[0:i],T1[0:i],'b.',label=r'$T_1$ measured')
        plt.plot(tm[0:i],T2[0:i],'r.',label=r'$T_2$ measured')
        plt.ylabel(r'Temperature ($^oC$)')
        plt.legend(loc=4)
        ax=plt.subplot(2,1,2)
        ax.grid()
        plt.plot(tm[0:i],Q1[0:i],'b-',label=r'$Q_1$')
        plt.plot(tm[0:i],Q2[0:i],'r:',label=r'$Q_2$')
        plt.ylabel('Heater (%)')
        plt.legend(loc=1)
        plt.xlabel('Time (sec)')
        plt.draw()
        plt.pause(0.05)

    # Turn off heaters
    a.Q1(0)
    a.Q2(0)
    a.close()
    # Save text file
    save_txt(tm[0:i],Q1[0:i],Q2[0:i],T1[0:i],T2[0:i],Tsp1[0:i],Tsp2[0:i])
    # Save figure
    plt.savefig('PID_Control.png')

# Allow user to end loop with Ctrl-C           
except KeyboardInterrupt:
    # Disconnect from Arduino
    a.Q1(0)
    a.Q2(0)
    print('Shutting down')
    a.close()
    save_txt(tm[0:i],Q1[0:i],Q2[0:i],T1[0:i],T2[0:i],Tsp1[0:i],Tsp2[0:i])
    plt.savefig('PID_Control.png')

# Make sure serial connection closes with an error
except:           
    # Disconnect from Arduino
    a.Q1(0)
    a.Q2(0)
    print('Error: Shutting down')
    a.close()
    save_txt(tm[0:i],Q1[0:i],Q2[0:i],T1[0:i],T2[0:i],Tsp1[0:i],Tsp2[0:i])
    plt.savefig('PID_Control.png')
    raise