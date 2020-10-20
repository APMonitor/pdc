import tclab
import numpy as np
import time
import matplotlib.pyplot as plt

# Heater 1 Model
Kp1 = 0.9      # degC/%
tauP1 = 175.0  # seconds
thetaP1 = 15   # seconds (integer)

# Heater 2 Model
Kp2 =          # degC/%
tauP2 =        # seconds
thetaP2 =      # seconds (integer)

# Steady-State Conditions
Tss = 23       # degC (ambient temperature)
Qss = 0        # % heater

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

# Temperature (K)
T1 = np.ones(loops) * a.T1 # measured T (degC)
T2 = np.ones(loops) * a.T2 # measured T (degC)

# Predictions
Tpl = np.ones(loops) * a.T1
Tp2 = np.ones(loops) * a.T2

# step tests (0 - 100%)
Q1 = np.ones(loops) * 0.0
Q1[350:450] = 20.0

Q2 = np.ones(loops) * 0.0
Q2[10:110] = 50.0 
Q2[200:300] = 90.0
Q2[400:500] = 70.0

print('Running Main Loop. Ctrl-C to end.')
print('  Time   Q1     Q2    T1     T2')
print('{:6.1f} {:6.2f} {:6.2f} {:6.2f} {:6.2f}'.format(tm[0], \
                                                       Q1[0], \
                                                       Q2[0], \
                                                       T1[0], \
                                                       T2[0]))

# Create plot
plt.figure(figsize=(10,7))
plt.ion()
plt.show()

# Main Loop
start_time = time.time()
prev_time = start_time
try:
    for i in range(1,loops):
        # Sleep time
        sleep_max = 1.0
        sleep = sleep_max - (time.time() - prev_time)
        if sleep>=0.01:
            time.sleep(sleep-0.01)
        else:
            time.sleep(0.01)

        # Record time and change in time
        t = time.time()
        dt = t - prev_time
        prev_time = t
        tm[i] = t - start_time

        # Read temperatures in Kelvin 
        T1[i] = a.T1
        T2[i] = a.T2

        # Simulate one time step with FOPDT models
        z = np.exp(-dt/tauP1)
        Tpl[i] = (Tpl[i-1]-Tss) * z \
                 + (Q1[max(0,i-int(thetaP1)-1)]-Qss)*(1-z)*Kp1 \
                 + Tss
        z = np.exp(-dt/tauP2)
        Tp2[i] = (Tp2[i-1]-Tss) * z \
                 + (Q2[max(0,i-int(thetaP2)-1)]-Qss)*(1-z)*Kp2 \
                 + Tss

        # Write output (0-100)
        a.Q1(Q1[i])
        a.Q2(Q2[i])

        # Print line of data
        print('{:6.1f} {:6.2f} {:6.2f} {:6.2f} {:6.2f}'.format(tm[i], \
                                                               Q1[i], \
                                                               Q2[i], \
                                                               T1[i], \
                                                               T2[i]))

        # Plot
        plt.clf()
        ax=plt.subplot(2,1,1)
        ax.grid()
        plt.plot(tm[0:i],T1[0:i],'r.',label=r'$T_1$ measured')
        plt.plot(tm[0:i],Tpl[0:i],'g:',label=r'$T_1$ FOPDT')
        plt.plot(tm[0:i],T2[0:i],'b.',label=r'$T_2$ measured')
        plt.plot(tm[0:i],Tp2[0:i],'k--',label=r'$T_2$ FOPDT')
        plt.ylabel(r'Temperature ($^o$C)')
        plt.legend(loc=2)
        ax=plt.subplot(2,1,2)
        ax.grid()
        plt.plot(tm[0:i],Q1[0:i],'r-',label=r'$Q_1$')
        plt.plot(tm[0:i],Q2[0:i],'b:',label=r'$Q_2$')
        plt.ylabel('Heaters')
        plt.xlabel('Time (sec)')
        plt.legend(loc='best')
        plt.draw()
        plt.pause(0.05)

    # Turn off heaters
    a.Q1(0)
    a.Q2(0)
    # Save figure
    plt.savefig('heater_test.png')

# Allow user to end loop with Ctrl-C           
except KeyboardInterrupt:
    # Disconnect from Arduino
    a.Q1(0)
    a.Q2(0)
    plt.savefig('heater_test.png')
    print('Shutting down')
    a.close()

# Make sure serial connection still closes when there's an error
except:           
    # Disconnect from Arduino
    a.Q1(0)
    a.Q2(0)
    plt.savefig('heater_test.png')
    print('Error: Shutting down')
    a.close()
    raise