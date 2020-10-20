from gekko import GEKKO    
m = GEKKO(remote=False)

# create variables
x1,x2,x3,x4 = m.Array(m.Var,4,lb=1,ub=5)

# initial values
x1.value = 1; x2.value = 5; x3.value = 5; x4.value = 1

m.Equation(x1*x2*x3*x4>=25)
m.Equation(x1**2+x2**2+x3**2+x4**2==40)
m.Minimize(x1*x4*(x1+x2+x3)+x3)
m.solve(disp=False)

print('Results')
print('x1: ' + str(x1.value[0])); print('x2: ' + str(x2.value[0]))
print('x3: ' + str(x3.value[0])); print('x4: ' + str(x4.value[0]))