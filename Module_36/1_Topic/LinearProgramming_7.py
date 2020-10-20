# Import APM Python library "pip install APMonitor"
from APMonitor.apm import *

# Select the server
server = 'https://byu.apmonitor.com'

# Give the application a name
app = 'production'

# Clear any previous applications by that name
apm(server,app,'clear all')

# Write the model file
fid = open('softdrink.apm','w')
fid.write('Variables \n')
fid.write('  x1 > 0 , < 5  ! Product 1 \n')
fid.write('  x2 > 0 , < 4  ! Product 2 \n')
fid.write('  profit \n')
fid.write(' \n')
fid.write('Equations \n')
fid.write('  ! profit function \n')
fid.write('  maximize profit   \n')
fid.write('  profit = 100 * x1 + 125 * x2 \n')
fid.write('  3 * x1 + 6 * x2 <= 30 \n')
fid.write('  8 * x1 + 4 * x2 <= 44         \n')
fid.close()
apm_load(server,app,'softdrink.apm')

# Solve on APM server
solver_output = apm(server,app,'solve')

# Display solver output
print(solver_output)

# Retrieve results
sol = apm_sol(server,app)

print ('')
print ('--- Results of the Optimization Problem ---')
print ('Product 1 (x1): ' + str(sol['x1']))
print ('Product 2 (x2): ' + str(sol['x2']))
print ('Profit: ' + str(sol['profit']))

# Display Results in Web Viewer 
url = apm_web_var(server,app)

## Generate a contour plot
# Import some other libraries that we'll need
# matplotlib and numpy packages must also be installed
import matplotlib
import numpy as np
import matplotlib.pyplot as plt

# Design variables at mesh points
x = np.arange(-1.0, 8.0, 0.02)
y = np.arange(-1.0, 6.0, 0.02)
x1, x2 = np.meshgrid(x,y)

# Equations and Constraints
profit = 100.0 * x1 + 125.0 * x2
A_usage = 3.0 * x1 + 6.0 * x2
B_usage = 8.0 * x1 + 4.0 * x2

# Create a contour plot
plt.figure()
# Weight contours
lines = np.linspace(100.0,800.0,8)
CS = plt.contour(x1,x2,profit,lines,colors='g')
plt.clabel(CS, inline=1, fontsize=10)
# A usage < 30
CS = plt.contour(x1,x2,A_usage,[26.0, 28.0, 30.0],colors='r',linewidths=[0.5,1.0,4.0])
plt.clabel(CS, inline=1, fontsize=10)
# B usage < 44
CS = plt.contour(x1, x2,B_usage,[40.0,42.0,44.0],colors='b',linewidths=[0.5,1.0,4.0])
plt.clabel(CS, inline=1, fontsize=10)
# Container for 0 <= Product 1 <= 500 L
CS = plt.contour(x1, x2,x1 ,[0.0, 0.1, 4.9, 5.0],colors='k',linewidths=[4.0,1.0,1.0,4.0])
plt.clabel(CS, inline=1, fontsize=10)
# Container for 0 <= Product 2 <= 400 L
CS = plt.contour(x1, x2,x2 ,[0.0, 0.1, 3.9, 4.0],colors='k',linewidths=[4.0,1.0,1.0,4.0])
plt.clabel(CS, inline=1, fontsize=10)

# Add some labels
plt.title('Soft Drink Production Problem')
plt.xlabel('Product 1 (100 L)')
plt.ylabel('Product 2 (100 L)')
# Save the figure as a PNG
plt.savefig('contour.png')

# Show the plots
plt.show()