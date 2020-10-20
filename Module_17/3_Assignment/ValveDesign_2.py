import numpy as np
import matplotlib.pyplot as plt

DPt = 100    # Total pressure generated by pump (constant)
Cv = 2       # Valve Cv
g_s = 1.1    # specific gravity of fluid
lift = np.linspace(0,1)  # equally spaced points between 0 and 1

## Lift functions for two different valve trim types
def f_lin(x):
    return x             # linear valve trim
def f_ep(x):
    R = 20
    return R**(x-1)      # equal percentage valve trim (R = 20-50)

## Installed valve performance
# pressure drop across the system (without valve)
c1 = 2
def DPe(q):
    return c1 * q**2

# valve and process equipment flow with 100 bar pressure drop
def qi(x,f,Cv):
    return np.sqrt((Cv*f(x))**2*DPt / (g_s + (Cv*f(x))**2 * c1))

# Process equipment + Valve performance
flow_lin = qi(lift,f_lin,Cv)  # flow through linear valve
flow_ep  = qi(lift,f_ep,Cv)   # flow through equal percentage valve

plt.figure(2)
plt.title('Valve Performance - Installed')
plt.subplot(3,1,1)
plt.plot(lift,flow_lin,'b-',label='Linear Valve')
plt.plot(lift,flow_ep,'r--',label='Equal Percentage Valve')
plt.plot([0,1],[0,6.5],'k-',linewidth=2,label='Desired Profile')
plt.legend(loc='best')
plt.ylabel('Flow')

plt.subplot(3,1,2)
plt.plot(lift,DPt-DPe(flow_lin),'k:',linewidth=3)
plt.plot(lift,DPe(flow_lin),'r--',linewidth=3)
plt.legend(['Linear Valve','Process Equipment'],loc='best')
plt.ylabel(r'$\Delta P$')

plt.subplot(3,1,3)
plt.plot(lift,DPt-DPe(flow_ep),'k:',linewidth=3)
plt.plot(lift,DPe(flow_ep),'r--',linewidth=3)
plt.legend(['Equal Percentage Valve','Process Equipment'],loc='best')
plt.ylabel(r'$\Delta P$')
plt.xlabel('Lift')

plt.show()