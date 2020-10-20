import tclab
import time
import numpy as np
from simple_pid import PID

# Connect to Arduino
a = tclab.TCLab()

# Create PID controller
pid = PID(Kp=2,Ki=2/136,Kd=0,\
          setpoint=40,sample_time=1.0,output_limits=(0,100))

for i in range(300):        # 5 minutes (300 sec)
    # pid control
    OP = pid(a.T1)
    a.Q1(OP)

    # print line
    print('Heater: ' + str(round(OP,2)) + '%' + \
          ' T PV: '  + str(a.T1) + 'degC' + \
          ' T SP: '  + str(pid.setpoint) + 'degC')

    # wait for next sample time
    time.sleep(pid.sample_time)