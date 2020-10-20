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
    Q2d[120:320] = 100
    Q2d[320:520] = 10
    Q2d[520:] = 80

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
        # close connection to Arduino
        a.close()
        fid.close()
    except:
        filename = 'https://apmonitor.com/pdc/uploads/Main/tclab_data2.txt'
    # read either local file or use link if no TCLab
    data = pd.read_csv(filename)

# Fit Parameters of Energy Balance
m = GEKKO() # Create GEKKO Model

# Parameters to Estimate
U = m.FV(value=10,lb=1,ub=20)
Us = m.FV(value=20,lb=5,ub=40)
alpha1 = m.FV(value=0.01,lb=0.001,ub=0.03)  # W / % heater
alpha2 = m.FV(value=0.005,lb=0.001,ub=0.02) # W / % heater
tau = m.FV(value=10.0,lb=5.0,ub=60.0)

# Measured inputs
Q1 = m.Param()
Q2 = m.Param()

Ta =23.0+273.15                     # K
mass = 4.0/1000.0                   # kg
Cp = 0.5*1000.0                     # J/kg-K    
A = 10.0/100.0**2                   # Area not between heaters in m^2
As = 2.0/100.0**2                   # Area between heaters in m^2
eps = 0.9                           # Emissivity
sigma = 5.67e-8                     # Stefan-Boltzmann

TH1 = m.SV()
TH2 = m.SV()
TC1 = m.CV()
TC2 = m.CV()

# Heater Temperatures in Kelvin
T1 = m.Intermediate(TH1+273.15)
T2 = m.Intermediate(TH2+273.15)

# Heat transfer between two heaters
Q_C12 = m.Intermediate(Us*As*(T2-T1)) # Convective
Q_R12 = m.Intermediate(eps*sigma*As*(T2**4-T1**4)) # Radiative

# Energy balances
m.Equation(TH1.dt() == (1.0/(mass*Cp))*(U*A*(Ta-T1) \
                + eps * sigma * A * (Ta**4 - T1**4) \
                + Q_C12 + Q_R12 \
                + alpha1*Q1))

m.Equation(TH2.dt() == (1.0/(mass*Cp))*(U*A*(Ta-T2) \
                + eps * sigma * A * (Ta**4 - T2**4) \
                - Q_C12 - Q_R12 \
                + alpha2*Q2))

# Conduction to temperature sensors
m.Equation(tau*TC1.dt() == TH1-TC1)
m.Equation(tau*TC2.dt() == TH2-TC2)

# Options
# STATUS=1 allows solver to adjust parameter
U.STATUS = 1  
Us.STATUS = 1  
alpha1.STATUS = 1 
alpha2.STATUS = 1
tau.STATUS = 1

Q1.value=data['Q1'].values
Q2.value=data['Q2'].values
TH1.value=data['T1'].values[0]
TH2.value=data['T2'].values[0]
TC1.value=data['T1'].values
TC1.FSTATUS = 1    # minimize fstatus * (meas-pred)^2
TC2.value=data['T2'].values
TC2.FSTATUS = 1    # minimize fstatus * (meas-pred)^2

m.time = data['Time'].values
m.options.IMODE   = 5 # MHE
m.options.EV_TYPE = 2 # Objective type
m.options.NODES   = 2 # Collocation nodes
m.options.SOLVER  = 3 # IPOPT

m.solve(disp=False) # Solve physics-based model

# Parameter values
print('Estimated Parameters')
print('U     : ' + str(U.value[0]))
print('Us     : ' + str(Us.value[0]))
print('alpha1: ' + str(alpha1.value[0]))
print('alpha2: ' + str(alpha2.value[-1]))
print('tau: ' + str(tau.value[0]))

print('Constants')
print('Ta: ' + str(Ta))
print('m: ' + str(mass))
print('Cp: ' + str(Cp))
print('A: ' + str(A))
print('As: ' + str(As))
print('eps: ' + str(eps))
print('sigma: ' + str(sigma))

sae = 0.0
for i in range(len(data)):
    sae += np.abs(data['T1'][i]-TC1.value[i])
    sae += np.abs(data['T2'][i]-TC2.value[i])
print('SAE Energy Balance: ' + str(sae))

# Create plot
plt.figure(figsize=(10,7))
ax=plt.subplot(2,1,1)
ax.grid()
plt.plot(data['Time'],data['T1'],'r.',label=r'$T_1$ measured')
plt.plot(m.time,TC1.value,color='black',linestyle='--',\
         linewidth=2,label=r'$T_1$ energy balance')
plt.plot(data['Time'],data['T2'],'b.',label=r'$T_2$ measured')
plt.plot(m.time,TC2.value,color='orange',linestyle='--',\
         linewidth=2,label=r'$T_2$ energy balance')
plt.ylabel(r'T ($^oC$)')
plt.legend(loc=2)
ax=plt.subplot(2,1,2)
ax.grid()
plt.plot(data['Time'],data['Q1'],'r-',\
         linewidth=3,label=r'$Q_1$')
plt.plot(data['Time'],data['Q2'],'b:',\
         linewidth=3,label=r'$Q_2$')
plt.ylabel('Heaters')
plt.xlabel('Time (sec)')
plt.legend(loc='best')
plt.savefig('tclab_2nd_order_physics.png')
plt.show()