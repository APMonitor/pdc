import numpy as np
from scipy import signal
import matplotlib.pyplot as plt

# open loop
num = [-2.0]
den = [1.0,3.0,4.0,3.0,1.0]
sys = signal.TransferFunction(num, den)
t1,y1 = signal.step(sys)

plt.figure(1)
plt.plot(t1,y1,'k-')
plt.legend(['Open Loop'],loc='best')

# closed loop
plt.figure(2)
n = 6
Kc = np.linspace(-1.1,0.6,n)  # Kc values
t = np.linspace(0,100,1000) # time values
for i in range(n):
    num = [-2.0*Kc[i]]
    den = [1.0,3.0,4.0,3.0,1.0-2.0*Kc[i]]
    sys2 = signal.TransferFunction(num, den)
    t2,y2 = signal.step(sys2,T=t)
    plt.plot(t2,y2,label='Kc='+str(Kc[i]))
plt.ylim([-2,3])
plt.legend(loc='best')
plt.xlabel('Time')

# root locus plot
import numpy.polynomial.polynomial as poly
n = 1000  # number of points to plot
nr = 4    # number of roots
rs = np.zeros((n,2*nr))   # store results
Kc1 = -2.0
Kc2 = 1.0
Kc = np.linspace(Kc1,Kc2,n)  # Kc values
for i in range(n):        # cycle through n times
    den = [1.0,3.0,4.0,3.0,1.0-2.0*Kc[i]]
    roots = poly.polyroots(den) # find roots
    for j in range(nr):   # store roots
        rs[i,j] = roots[j].real # store real
        rs[i,j+nr] = roots[j].imag # store imaginary

plt.figure(3)
plt.xlabel('Root (real)')
plt.ylabel('Root (imag)')
plt.grid(b=True, which='major', color='b', linestyle='-')
plt.grid(b=True, which='minor', color='r', linestyle='--')
for i in range(nr):
    plt.plot(rs[:,i],rs[:,i+nr],'.')
plt.xlim([-1.5,0.5])
plt.ylim([-1.2,1.2])

plt.figure(4)
plt.subplot(2,1,1)
for i in range(nr):
    plt.plot(Kc,rs[:,i],'.')
plt.ylabel('Root (real part)')
plt.xlabel('Controller Gain (Kc)')
plt.xlim([Kc1,Kc2])
plt.ylim([-1,1])

plt.subplot(2,1,2)
for i in range(nr):
    plt.plot(Kc,rs[:,i+nr],'.')
plt.ylabel('Root (imag part)')
plt.xlabel('Controller Gain (Kc)')
plt.xlim([Kc1,Kc2])
plt.ylim([-2,2])


# bode plot
w,mag,phase = signal.bode(sys)
plt.figure(5)
plt.subplot(2,1,1)
plt.semilogx(w,mag,'k-',linewidth=3)
plt.grid(b=True, which='major', color='b', linestyle='-')
plt.grid(b=True, which='minor', color='r', linestyle='--')
plt.ylabel('Magnitude')

plt.subplot(2,1,2)
plt.semilogx(w,phase,'k-',linewidth=3)
plt.grid(b=True, which='major', color='b', linestyle='-')
plt.grid(b=True, which='minor', color='r', linestyle='--')
plt.ylabel('Phase')
plt.xlabel('Frequency')

plt.show()