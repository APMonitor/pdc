import numpy as np
from scipy.integrate import odeint
def model(y,t):
    k = 0.3
    return -k * y
y = odeint(model,5,[0,3])