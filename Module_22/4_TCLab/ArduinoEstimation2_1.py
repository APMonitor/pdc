import numpy as np
import pandas as pd
import tclab
import time
import os.path

# generate step test data on Arduino
filename = 'data.csv'

# redo data collection?
redo = False

# check if file already exists
if os.path.isfile(filename) and (not redo):
    print('File: '+filename+' already exists.')
    print('Change redo=True to collect data again')
    print('TCLab should be at room temperature at start')
else:
    # heater steps
    Q1d = np.zeros(601)
    Q1d[10:200] = 80
    Q1d[200:280] = 20
    Q1d[280:400] = 70
    Q1d[400:] = 50

    Q2d = np.zeros(601)
    Q2d[120:320] = 100
    Q2d[320:520] = 10
    Q2d[520:] = 80

    # Connect to Arduino
    a = tclab.TCLab()
    fid = open(filename,'w')
    fid.write('Time,Q1,Q2,T1,T2\n')
    fid.close()

    # run step test (10 min)
    for i in range(601):
        # set heater values
        a.Q1(Q1d[i])
        a.Q2(Q2d[i])
        print('Time: ' + str(i) + \
              ' Q1: ' + str(Q1d[i]) + \
              ' Q2: ' + str(Q2d[i]) + \
              ' T1: ' + str(a.T1)   + \
              ' T2: ' + str(a.T2))
        # wait 1 second
        time.sleep(1)
        fid = open(filename,'a')
        fid.write(str(i)+','+str(Q1d[i])+','+str(Q2d[i])+',' \
                  +str(a.T1)+','+str(a.T2)+'\n')
    # close connection to Arduino
    a.close()
    fid.close()