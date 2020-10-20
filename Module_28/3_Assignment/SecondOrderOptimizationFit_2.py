import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from gekko import GEKKO

# Import data file
# Column 1 = time (t)
# Column 2 = output (ymeas)
url = 'https://apmonitor.com/pdc/uploads/Main/data_2nd_order.txt'
data = pd.read_csv(url)
t = np.array(data['time'])
ymeas = np.array(data['output (y)'])

# Create GEKKO model
m = GEKKO()
m.time = t

# Inputs
u = 2 # step input
ym = m.Param(ymeas)

# estimate parameters Kp and taup
Kp = m.FV()
taup = m.FV(lb=0)
# turn on parameters (STATUS=1) to let optimize change them
Kp.STATUS = 1
taup.STATUS = 1

# Equation 1
y1 = m.Var(0.0)
m.Equation(taup*y1.dt()==-y1+Kp*u)

# Equation 2
y2 = m.Var(0.0)
m.Equation(y2.dt()+y2==-2*u)

# Summation
y = m.Var(0.0)
m.Equation(y==y1+y2)

# Minimize Objective
m.Obj((y-ym)**2)

# Optimize Kp, taup
m.options.IMODE=5
m.options.NODES=3
m.solve()

# show final objective
print('Final SSE Objective: ' + str(m.options.OBJFCNVAL))

print('Kp: ' + str(Kp.value[0]))
print('taup: ' + str(taup.value[0]))

# plot results
plt.figure()
plt.plot(t,y.value,'r-',linewidth=3,label='Predicted')
plt.plot(t,ymeas,'ko',linewidth=2,label='Measured')
plt.ylabel('Output')
plt.xlabel('Time')
plt.legend(loc='best')
plt.savefig('optimized.png')
plt.show()