import matplotlib.pyplot as plt
import numpy as np

K = 1
tau = 0.5
n = 81
t = np.linspace(0,8,n)
s1 = np.zeros(n)
s1[11:] = 1.0
s2 = np.zeros(n)
s2[51:] = 1.0

y = 3*K*(1-np.exp(-(t-1)/tau))*s1 \
   -3*K*(1-np.exp(-(t-5)/tau))*s2

plt.figure(1)
plt.plot([0,1,1.001,5,5.001,8],[0,0,3,3,0,0],'b-',linewidth=2)
plt.plot(t,y,'r--')
plt.ylabel('y(t)')
plt.xlabel('time (t)')
plt.legend(['u(t)','y(t)'])
plt.grid()
plt.savefig('fig1.png')

plt.show()