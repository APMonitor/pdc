import tclab
import time
a = tclab.TCLab() # connect to TCLab
fid = open('data.csv','w')
fid.write('Time,Q1,T1\n')
fid.write('0,0,'+str(a.T1)+'\n')
fid.close()
for i in range(240):  # 4 minute test
    time.sleep(1)
    T1 = a.T1 # temperature
    Q1 = 100 if T1<=40.0 else 0 # On/Off Control
    a.Q1(Q1) # set heater
    print('Time: '+str(i)+' Q1: '+str(Q1)+' T1 (SP=40): '+str(T1))
    fid = open('data.csv','a')
    fid.write(str(i)+','+str(Q1)+','+str(T1)+'\n')
    fid.close()
a.close()