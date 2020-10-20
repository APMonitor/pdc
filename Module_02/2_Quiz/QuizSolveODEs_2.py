import numpy as np
from scipy.integrate import odeint
n=31 # total time points
def model(y,t):
    return -0.3 * y
y=np.empty(n); t=np.empty(n)
for i in range(n):
    if i==0:
        t[i] = 0.0  # initial time
        y[i] = 5    # initial condition
    else:
        # integrate forward with time-step 0.1
        t[i] = t[i-1]+0.1
        y[i] = odeint(model,y[i-1],[t[i-1],t[i]])[-1]