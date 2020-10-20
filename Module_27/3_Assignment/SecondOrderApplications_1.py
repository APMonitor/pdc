import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
from scipy.integrate import odeint

# Change these values based on graphical fit
Kp = 1.0
taus = 1.0
zeta = 1.0

# Transfer Function
#  Kp / (taus * s**2 + 2 * zeta * taus * s + 1) 
num = [Kp]
den = [taus**2,2.0*zeta*taus,1]
sys1 = signal.TransferFunction(num,den)
t1,y1 = signal.step(sys1)

plt.figure(1)
plt.plot(t1,y1,'b--',linewidth=3,label='Transfer Fcn')
plt.xlabel('Time')
plt.ylabel('Response (y)')
plt.legend(loc='best')
plt.show()