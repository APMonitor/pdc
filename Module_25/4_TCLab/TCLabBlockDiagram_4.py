import sympy as sym
from sympy.abc import s,t,x,y,z
import numpy as np
from sympy.integrals import inverse_laplace_transform
import matplotlib.pyplot as plt

# Define inputs
# Setpoint step (up) starts at 1 sec
TSP = 20/s*sym.exp(-s)

# Transfer functions
Kc = 2.0
tauI = 180.0
Gc = Kc * (tauI*s+1)/(tauI*s)
delay = 1/(15*s+1) # Taylor series approx
Gp = delay * 0.9/(180*s+1)

# Closed loop response
Gc = Gc*Gp/(1+Gc*Gp)

# Calculate response
T1 = Gc * TSP

# Inverse Laplace Transform
tsp = inverse_laplace_transform(TSP,s,t)
t1 = inverse_laplace_transform(T1,s,t)
print('Temperature Solution')
print(t1)

# generate data for plot
tm = np.linspace(0,600,100)
TSPplot = np.zeros(len(tm))
T1plot = np.zeros(len(tm))

# substitute numeric values
for i in range(len(tm)):
    TSPplot[i] = tsp.subs(t,tm[i]) + 23.0
    T1plot[i] = t1.subs(t,tm[i]) + 23.0

# plot results
plt.figure()
plt.plot(tm/60,TSPplot,'k:',label='T1 Setpoint')
plt.plot(tm/60,T1plot,'b-',label='T1 Predicted')
plt.legend()
plt.xlabel('Time (min)')
plt.ylabel(r'Temperature Change $(\Delta T \, ^oC)$')
plt.show()