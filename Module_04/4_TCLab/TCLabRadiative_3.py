import numpy as np
import matplotlib.pyplot as plt
import tclab
import time
# pip install gekko
from gekko import GEKKO 

n = 300  # Number of second time points (5 min)

# collect data if TCLab is connected
try:
    lab = tclab.TCLab()
    T1 = [lab.T1]
    lab.Q1(50)
    for i in range(n):
        time.sleep(1)
        print(lab.T1)
        T1.append(lab.T1)
    lab.close()
    connected = True
except:
    print('Connect TCLab to Get Data')
    connected = False

# simulation
m = GEKKO()
m.time = np.linspace(0,n,n+1)
U = 5.0; A = 0.0012; Cp = 500 
mass = 0.004; alpha = 0.01; Ta = 23
eps = 0.9; sigma = 5.67e-8; TaK = Ta+273.15
TC = m.Var(Ta)
TK = m.Intermediate(TC+273.15)
conv = m.Intermediate(U*A*(Ta-TC))
rad  = m.Intermediate(sigma*eps*A*(TaK**4-TK**4))
loss = m.Intermediate(conv + rad)
gain = m.Intermediate(alpha*50)
m.Equation(mass*Cp*TC.dt()==conv+rad+gain)
m.options.NODES = 3
m.options.IMODE = 4 # dynamic simulation
m.solve(disp=False)

# Plot results
plt.figure()
plt.subplot(2,1,1)
plt.plot(m.time,TC,'b-',label='Simulated')
if connected:
    plt.plot(m.time,T1,'r.',label='Measured')
plt.ylabel(r'Temperature ($^oC$)')
plt.legend()
plt.subplot(2,1,2)
plt.plot(m.time,conv,'g:',label='Convection')
plt.plot(m.time,rad,'r--',label='Radiation')
plt.plot(m.time,loss,'k-',label='Total Lost')
plt.text(150,-0.1,'Heater input = '+str(gain.value[0])+' W')
plt.ylabel(r'Heat Loss (W)')
plt.legend(loc=3)
plt.xlabel('Time (sec)')
plt.show()