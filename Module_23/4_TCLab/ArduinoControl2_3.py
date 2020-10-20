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
Kff  = -0.3

# Animate Plot?
animate = True
if animate:
    try:
        from IPython import get_ipython
        from IPython.display import display,clear_output
        get_ipython().run_line_magic('matplotlib', 'inline')
        ipython = True
        print('IPython Notebook')
    except:
        ipython = False
        print('Not IPython Notebook')

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
def pid(sp,pv,pv_last,ierr,dt,d,cid):
    # Parameters in terms of PID coefficients
    if cid==1:
        # controller 1
        KP = Kc
        Kf = Kff
    else:
        # controller 2
        KP = Kc * 2.0
        Kf = Kff * 2.0
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

# Wait until temperature is below 25 degC
print('Check that temperatures are < 25 degC before starting')
i = 0
while a.T1>=25.0 or a.T2>=25.0:
    print(f'Time: {i} T1: {a.T1} T2: {a.T2}')
    i += 10
    time.sleep(10)

# Turn LED on
print('LED On')
a.LED(100)

# Run time in minutes
run_time = 10.0

# Number of cycles
loops = int(60.0*run_time)
tm = np.zeros(loops)

# Heater set point steps
Tsp1 = np.ones(loops) * a.T1
Tsp2 = np.ones(loops) * a.T2 # set point (degC)
Tsp1[10:] = 60.0         # step up
Tsp1[400:] = 40.0        # step down
Tsp2[150:] = 50.0        # step up
Tsp2[350:] = 35.0        # step down

T1 = np.ones(loops) * a.T1 # measured T (degC)
T2 = np.ones(loops) * a.T2 # measured T (degC)

# impulse tests (0 - 100%)
Q1 = np.ones(loops) * 0.0
Q2 = np.ones(loops) * 0.0

if not animate:
    print('Running Main Loop. Ctrl-C to end.')
    print('  Time    SP1    PV1     Q1    SP2    PV2     Q2    IAE')
    print(('{:6.1f} {:6.2f} {:6.2f} ' + \
           '{:6.2f} {:6.2f} {:6.2f} {:6.2f} {:6.2f}').format( \
               tm[0],Tsp1[0],T1[0],Q1[0],Tsp2[0],T2[0],Q2[0],0.0))

# Main Loop
start_time = time.time()
prev_time = start_time
dt_error = 0.0
# Integral error
ierr1 = 0.0
ierr2 = 0.0
# Integral absolute error
iae = 0.0

if not ipython:
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
            dt_error = dt-sleep_max+0.009
        else:
            dt_error = 0.0
        prev_time = t
        tm[i] = t - start_time

        # Read temperatures in Kelvin 
        T1[i] = a.T1
        T2[i] = a.T2

        # Disturbances
        d1 = T1[i] - 23.0
        d2 = T2[i] - 23.0

        # Integral absolute error
        iae += np.abs(Tsp1[i]-T1[i]) + np.abs(Tsp2[i]-T2[i])

        # Calculate PID output
        [Q1[i],P,ierr1,D,FF] = pid(Tsp1[i],T1[i],T1[i-1],ierr1,dt,d2,1)
        [Q2[i],P,ierr2,D,FF] = pid(Tsp2[i],T2[i],T2[i-1],ierr2,dt,d1,2)

        # Write output (0-100)
        a.Q1(Q1[i])
        a.Q2(Q2[i])

        if not animate:
            # Print line of data
            print(('{:6.1f} {:6.2f} {:6.2f} ' + \
                  '{:6.2f} {:6.2f} {:6.2f} {:6.2f} {:6.2f}').format( \
                      tm[i],Tsp1[i],T1[i],Q1[i],Tsp2[i],T2[i],Q2[i],iae))
        else:
            if ipython:
                plt.figure(figsize=(10,7))
            else:
                plt.clf()
            # Update plot
            ax=plt.subplot(2,1,1)
            ax.grid()
            plt.plot(tm[0:i],Tsp1[0:i],'k--',label=r'$T_1$ set point')
            plt.plot(tm[0:i],T1[0:i],'b.',label=r'$T_1$ measured')
            plt.plot(tm[0:i],Tsp2[0:i],'k-',label=r'$T_2$ set point')
            plt.plot(tm[0:i],T2[0:i],'r.',label=r'$T_2$ measured')
            plt.ylabel(r'Temperature ($^oC$)')
            plt.text(0,65,'IAE: ' + str(np.round(iae,2)))
            plt.legend(loc=4)
            plt.ylim([15,70])
            ax=plt.subplot(2,1,2)
            ax.grid()
            plt.plot(tm[0:i],Q1[0:i],'b-',label=r'$Q_1$')
            plt.plot(tm[0:i],Q2[0:i],'r:',label=r'$Q_2$')
            plt.ylim([-10,110])
            plt.ylabel('Heater (%)')
            plt.legend(loc=1)
            plt.xlabel('Time (sec)')
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
    # Save text file
    save_txt(tm,Q1,Q2,T1,T2,Tsp1,Tsp2)
    # Save Plot
    if not animate:
        plt.figure(figsize=(10,7))
        ax=plt.subplot(2,1,1)
        ax.grid()
        plt.plot(tm,Tsp1,'k--',label=r'$T_1$ set point')
        plt.plot(tm,T1,'b.',label=r'$T_1$ measured')
        plt.plot(tm,Tsp2,'k-',label=r'$T_2$ set point')
        plt.plot(tm,T2,'r.',label=r'$T_2$ measured')
        plt.ylabel(r'Temperature ($^oC$)')
        plt.text(0,65,'IAE: ' + str(np.round(iae,2)))
        plt.legend(loc=4)
        ax=plt.subplot(2,1,2)
        ax.grid()
        plt.plot(tm,Q1,'b-',label=r'$Q_1$')
        plt.plot(tm,Q2,'r:',label=r'$Q_2$')
        plt.ylabel('Heater (%)')
        plt.legend(loc=1)
        plt.xlabel('Time (sec)')
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

print('PID test complete')
print('Kc: ' + str(Kc))
print('tauI: ' + str(tauI))
print('tauD: ' + str(tauD))
print('Kff: ' + str(Kff))