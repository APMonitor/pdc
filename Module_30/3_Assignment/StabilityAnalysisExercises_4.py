import numpy as np
from scipy import signal
import matplotlib.pyplot as plt

a = 0.08*0.75*30*0.7
n = 5
Kc = np.linspace(0.78,8.5,n)
tm = np.linspace(0,100,1000)
for Kci in Kc:
    num = [a*0.1*Kci,a*Kci]
    den = [0.2,2.1,0.9,-1+1.26*Kci]
    sys = signal.TransferFunction(num,den)
    t,y = signal.step(sys,T=tm)
    plt.plot(t,y,label='Kc='+str(Kci))
plt.legend(loc='best')
plt.xlim([0,100])
plt.ylim([-2,5])
plt.show()