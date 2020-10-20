import numpy as np
from gekko import GEKKO
import matplotlib.pyplot as plt

m = GEKKO()
u = m.FV(0.1)   # social distancing (0-1)
         # 0   = no social distancing
         # 0.1 = masks
         # 0.2 = masks and hybrid classes
         # 0.3 = masks, hybrid, and online classes

t_incubation = 5.1 
t_infective = 3.3 
R0 = 2.4 
N = 33517 

# initial number of infected and recovered individuals
e_initial = 1/N
i_initial = 0.00
r_initial = 0.00
s_initial = 1 - e_initial - i_initial - r_initial

alpha = 1/t_incubation
gamma = 1/t_infective
beta = R0*gamma

s,e,i,r = m.Array(m.Var,4)
s.value = s_initial
e.value = e_initial
i.value = i_initial
s.value = s_initial
m.Equations([s.dt()==-(1-u)*beta * s * i,\
             e.dt()== (1-u)*beta * s * i - alpha * e,\
             i.dt()==alpha * e - gamma * i,\
             r.dt()==gamma*i])

t = np.linspace(0, 200, 101)
t = np.insert(t,1,[0.001,0.002,0.004,0.008,0.02,0.04,0.08,\
                   0.2,0.4,0.8])
m.time = t
m.options.IMODE=7
m.options.NODES=3
m.solve(disp=False)

# plot the data
plt.figure(figsize=(8,5))
plt.subplot(2,1,1)
plt.title('Social Distancing = '+str(u.value[0]*100)+'%')
plt.plot(m.time, s.value, color='blue', lw=3, label='Susceptible')
plt.plot(m.time, r.value, color='red',  lw=3, label='Recovered')
plt.ylabel('Fraction')
plt.legend()

plt.subplot(2,1,2)
plt.plot(m.time, i.value, color='orange', lw=3, label='Infective')
plt.plot(m.time, e.value, color='purple', lw=3, label='Exposed')
plt.ylim(0, 0.2)
plt.xlabel('Time (days)')
plt.ylabel('Fraction')
plt.legend()

plt.show()