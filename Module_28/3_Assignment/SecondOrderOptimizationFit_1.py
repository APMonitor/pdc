import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import minimize

# Import data file
# Column 1 = time (t)
# Column 2 = output (ymeas)
url = 'https://apmonitor.com/pdc/uploads/Main/data_2nd_order.txt'
data = pd.read_csv(url)
t = np.array(data['time'])
ymeas = np.array(data['output (y)'])

def model(p):
    Kp = p[0]
    taup = p[1]
    # predicted values
    ypred = 2.0 * Kp * (1.0-np.exp(-t/taup)) \
            - 4.0 * (1-np.exp(-t))
    return ypred

def objective(p):
    ypred = model(p)    
    sse = sum((ymeas-ypred)**2)
    return sse

# initial guesses for Kp and taup
p0 = [1.0,1.0]

# show initial objective
print('Initial SSE Objective: ' + str(objective(p0)))

# optimize Kp, taup
solution = minimize(objective,p0)
p = solution.x

# show final objective
print('Final SSE Objective: ' + str(objective(p)))

print('Kp: ' + str(p[0]))
print('taup: ' + str(p[1]))

# calculate new ypred
ypred = model(p)

# plot results
plt.figure()
plt.plot(t,ypred,'r-',linewidth=3,label='Predicted')
plt.plot(t,ymeas,'ko',linewidth=2,label='Measured')
plt.ylabel('Output')
plt.xlabel('Time')
plt.legend(loc='best')
plt.savefig('optimized.png')
plt.show()