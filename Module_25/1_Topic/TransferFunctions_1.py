import sympy as sym
from sympy.abc import s,t,x,y,z
import numpy as np
from sympy.integrals import inverse_laplace_transform
import matplotlib.pyplot as plt

# Define inputs
# First step (up) starts at 1 sec
U1 = 2/s*sym.exp(-s)
# Ramp (down) starts at 3 sec
U2 = -1/s**2*sym.exp(-3*s)
# Ramp completes at 5 sec
U3 = 1/s**2*sym.exp(-5*s)

# Transfer function
G = 5*(s+1)/(s+3)**2

# Calculate responses
Y1 = G * U1
Y2 = G * U2
Y3 = G * U3

# Inverse Laplace Transform
u1 = inverse_laplace_transform(U1,s,t)
u2 = inverse_laplace_transform(U2,s,t)
u3 = inverse_laplace_transform(U3,s,t)
y1 = inverse_laplace_transform(Y1,s,t)
y2 = inverse_laplace_transform(Y2,s,t)
y3 = inverse_laplace_transform(Y3,s,t)
print('y1')
print(y1)

# generate data for plot
tm = np.linspace(0,8,100)
us = np.zeros(len(tm))
ys = np.zeros(len(tm))

# substitute numeric values for u and y
for u in [u1,u2,u3]:
    for i in range(len(tm)):
        us[i] += u.subs(t,tm[i])
for y in [y1,y2,y3]:
    for i in range(len(tm)):
        ys[i] += y.subs(t,tm[i])

# plot results
plt.figure()
plt.plot(tm,us,label='u(t)')
plt.plot(tm,ys,label='y(t)')
plt.legend()
plt.xlabel('Time')
plt.show()