from gekko import GEKKO

m = GEKKO()

# variables
x1 = m.Var(value=0 , lb=0 , ub=5 , name='x1') # Product 1
x2 = m.Var(value=0 , lb=0 , ub=4 , name='x2') # Product 2
profit = m.Var(value=1 , name='profit')

# profit function
m.Obj(-profit)
m.Equation(profit==100*x1+125*x2)
m.Equation(3*x1+6*x2<=30)
m.Equation(8*x1+4*x2<=44)

m.solve()

print ('')
print ('--- Results of the Optimization Problem ---')
print ('Product 1 (x1): ' + str(x1[0]))
print ('Product 2 (x2): ' + str(x2[0]))
print ('Profit: ' + str(profit[0]))

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