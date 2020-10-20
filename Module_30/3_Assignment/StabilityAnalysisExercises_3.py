import numpy as np
from scipy import signal
import matplotlib.pyplot as plt

name = 'Problem 1A'
num = [4.0]
p1 = np.poly1d([1,-1])
p2 = np.poly1d([1,2])
p3 = np.poly1d([1,3])
den = p1*p2*p3
sys = signal.TransferFunction(num,den)
t,y = signal.step(sys)
plt.figure(1)
plt.plot(t,y,'k-',label=name)
plt.legend(loc='best')

name = 'Problem 1B'
num = [1,-1,2]
p1 = [1,1]
p2 = [1,1,1]
den = p1
t = np.linspace(0,50,1000)
for i in range(9):
    den = np.convolve(den,p1)
den = np.convolve(den,p2)
print(den)
sys = signal.TransferFunction(num,den)
t,y = signal.step(sys,T=t)
plt.figure(2)
plt.plot(t,y,'k-',label=name)
plt.legend(loc='best')

name = 'Problem 1C'
num = [1]
p1 = np.poly1d([1,1])
p2 = np.poly1d([1,1,1])
den = p1*p2
print(den)
sys = signal.TransferFunction(num,den)
t,y = signal.step(sys,T=t)
plt.figure(3)
plt.plot(t,y,'k-',label=name)
plt.legend(loc='best')
plt.show()