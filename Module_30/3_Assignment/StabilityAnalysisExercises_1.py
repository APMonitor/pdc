import numpy as np
from scipy import signal
import matplotlib.pyplot as plt

name = 'Problem 1A'
num = [4.0]
p1 = [1,-1]
p2 = [1,2]
p3 = [1,3]
den = np.convolve(p1,p1)
den = np.convolve(den,p2)
den = np.convolve(den,p3)
sys = signal.TransferFunction(num, den)
t,y = signal.step(sys)

plt.figure(1)
plt.plot(t,y,'k-')
plt.legend([name],loc='best')
plt.xlabel('Time')
plt.show()