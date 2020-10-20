import tclab
import time
import numpy as np
from simple_pid import PID

# Connect to Arduino
a = tclab.TCLab()

# Create PID controllers
pid1 = PID(Kp=2,Ki=2/136,Kd=0,\
          setpoint=40,sample_time=1.0,output_limits=(0,100))
pid2 = PID(Kp=4,Ki=4/136,Kd=0,\
          setpoint=35,sample_time=1.0,output_limits=(0,100))

for i in range(600):        # 10 minutes (600 sec)
    # pid control
    OP1 = pid1(a.T1)
    OP2 = pid2(a.T2)
    a.Q1(OP1)
    a.Q2(OP2)

    # print line
    print('Heater: ' + str(round(OP1,2)) + '%' + \
          ' T1 PV: '  + str(a.T1) + 'degC' + \
          ' T1 SP: '  + str(pid1.setpoint) + 'degC')

    # wait for next sample time
    time.sleep(pid.sample_time)