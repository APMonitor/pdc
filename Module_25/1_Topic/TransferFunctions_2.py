from gekko import GEKKO
import numpy as np
import matplotlib.pyplot as plt

# Create GEKKO model
m = GEKKO()

# Time points for simulation
nt = 81
m.time = np.linspace(0,8,nt)

# Define input
# First step (up) starts at 1 sec
# Ramp (down) starts at 3 sec
# Ramp completes at 5 sec
ut = np.zeros(nt)
ut[11:31] = 2.0
for i in range(31,51):
    ut[i] = ut[i-1] - 0.1

# Define model
u = m.Param(value=ut)
ud = m.Var()
y = m.Var()
dydt = m.Var()
m.Equation(ud==u)
m.Equation(dydt==y.dt())
m.Equation(dydt.dt() + 6*y.dt() + 9*y==5*ud.dt()+5*u)

# Simulation options
m.options.IMODE=7
m.options.NODES=4
m.solve(disp=False)

# plot results
plt.figure()
plt.plot(m.time,u.value,label='u(t)')
plt.plot(m.time,y.value,label='y(t)')
plt.legend()
plt.xlabel('Time')
plt.show()