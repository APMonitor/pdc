import numpy as np
A = [[-0.2,-1,0.6],[5.0,1.0,-0.7],[1.0,0,-3.0]]
B = [[1],[0],[0]]; C = [0.5,0.5,0.5]; D = [0]
print(np.linalg.eig(A)[0])

from scipy import signal
sys1 = signal.StateSpace(A,B,C,D)
t1,y1 = signal.step(sys1)

import matplotlib.pyplot as plt
plt.figure(1)
plt.plot(t1,y1,'r-',label='y')
plt.legend()
plt.xlabel('Time')
plt.show()