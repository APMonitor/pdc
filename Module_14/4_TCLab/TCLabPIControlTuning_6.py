import tclab
import time
import numpy as np
from simple_pid import PID
import matplotlib.pyplot as plt

# process model
Kp = 0.9
taup = 175.0
thetap = 15.0

c = ['IMC','ITAE']

for xi,ci in enumerate(c):
    if ci=='IMC':
        # -----------------------------
        # Calculate Kc,tauI,tauD (IMC Aggressive)
        # -----------------------------
        tauc = max(0.1*taup,0.8*thetap)
        Kc = (1/Kp)*(taup)/(thetap+tauc)
        tauI = taup
        tauD = 0
    else:
        # -----------------------------
        # Calculate Kc,tauI,tauD (ITAE)
        # -----------------------------
        Kc = (0.586/Kp)*(thetap/taup)**(-0.916)
        tauI = taup/(1.03-0.165*(thetap/taup))
        tauD = 0

    print('Controller Tuning: ' + ci)
    print('Kc: ' + str(Kc))
    print('tauI: ' + str(tauI))
    print('tauD: ' + str(tauD))

    lab = tclab.TCLab()
    # Create PID controller
    pid = PID(Kp=Kc,Ki=Kc/tauI,Kd=Kc*tauD,\
              setpoint=23,sample_time=1.0,output_limits=(0,100))

    n = 600
    tm = np.linspace(0,n-1,n) # Time values
    T1 = np.zeros(n)
    Q1 = np.zeros(n)
    # step setpoint from 23.0 to 60.0 degC
    SP1 = np.ones(n)*23.0
    SP1[10:] = 60.0
    iae = 0.0

    print('Time OP    PV    SP')
    for i in range(n):
        pid.setpoint = SP1[i]
        T1[i] = lab.T1
        iae += np.abs(SP1[i]-T1[i])
        Q1[i] = pid(T1[i]) # PID control
        lab.Q1(Q1[i])
        print(i,round(Q1[i],2), T1[i], pid.setpoint)
        time.sleep(pid.sample_time) # wait 1 sec
    lab.close()

    # Save data file
    data = np.vstack((tm,Q1,T1,SP1)).T
    np.savetxt('PID_control_'+ci+'.csv',data,delimiter=',',\
               header='Time,Q1,T1,SP1',comments='')

    # Create Figure
    plt.figure(xi,figsize=(10,7))
    ax = plt.subplot(2,1,1)
    plt.title('PID Control with '+ci+' Tuning')
    ax.grid()
    plt.plot(tm/60.0,SP1,'k-',label=r'$T_1$ SP')
    plt.plot(tm/60.0,T1,'r.',label=r'$T_1$ PV')
    plt.text(5.1,25.0,'IAE: ' + str(round(iae,2)))
    plt.ylabel(r'Temp ($^oC$)')
    plt.legend(loc=2)
    ax = plt.subplot(2,1,2)
    ax.grid()
    plt.plot(tm/60.0,Q1,'b-',label=r'$Q_1$')
    plt.ylabel(r'Heater (%)')
    plt.xlabel('Time (min)')
    plt.legend(loc=1)
    plt.savefig('PID_Control_'+ci+'.png')
    print('Wait 10 min to cool down')
    time.sleep(600)

plt.show()