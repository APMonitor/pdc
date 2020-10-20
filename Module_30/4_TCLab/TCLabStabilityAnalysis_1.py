import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from gekko import GEKKO
import tclab
import time

# Import data
try:
    # try to read local data file first
    filename = 'data.csv'
    data = pd.read_csv(filename)
except:
    # heater steps
    Q1d = np.zeros(601)
    Q1d[10:200] = 80
    Q1d[200:280] = 20
    Q1d[280:400] = 70
    Q1d[400:] = 50

    Q2d = np.zeros(601)

    try:
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
            fid.close()
        # close connection to Arduino
        a.close()
    except:
        filename = 'https://apmonitor.com/pdc/uploads/Main/tclab_data3.txt'
    # read either local file or use link if no TCLab
    data = pd.read_csv(filename)

# Second order model of TCLab
m = GEKKO()
m.time = data['Time'].values
Kp   = m.FV(1.0,lb=0.5,ub=2.0)
taus = m.FV(50,lb=10,ub=200)
zeta =  m.FV(1.2,lb=1.1,ub=5)
T0 = data['T1'][0]
Q1 = m.Param(0)
x = m.Var(0); TC1 = m.CV(T0)
m.Equation(x==TC1.dt())
m.Equation((taus**2)*x.dt()+2*zeta*taus*TC1.dt()+(TC1-T0) == Kp*Q1)
m.options.IMODE = 5
m.options.NODES = 2
m.options.EV_TYPE = 2 # Objective type
Kp.STATUS = 1
taus.STATUS = 1
zeta.STATUS = 1
TC1.FSTATUS = 1
Q1.value=data['Q1'].values
TC1.value=data['T1'].values
m.solve(disp=True)

# Parameter values
print('Estimated Parameters')
print('Kp  : ' + str(Kp.value[0]))
print('taus: ' + str(taus.value[0]))
print('zeta: ' + str(zeta.value[0]))

# Create plot
plt.figure(figsize=(10,7))
ax=plt.subplot(2,1,1)
ax.grid()
plt.plot(data['Time'],data['T1'],'b.',label=r'$T_1$ measured')
plt.plot(m.time,TC1.value,color='orange',linestyle='--',\
         linewidth=2,label=r'$T_1$ second order')
plt.ylabel(r'T ($^oC$)')
plt.legend(loc=2)
ax=plt.subplot(2,1,2)
ax.grid()
plt.plot(data['Time'],data['Q1'],'r-',\
         linewidth=3,label=r'$Q_1$')
plt.ylabel('Heater (%)')
plt.xlabel('Time (sec)')
plt.legend(loc='best')
plt.savefig('tclab_2nd_order.png')
plt.show()