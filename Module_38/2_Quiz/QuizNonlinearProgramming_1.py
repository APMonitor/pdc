from scipy.optimize import minimize
def objective(x):
    return x[0]*x[3]*(x[0]+x[1]+x[2])+x[2]
def constraint1(x):
    return x[0]*x[1]*x[2]*x[3]-25.0
def constraint2(x):
    return 40.0 - sum([xi**2 for xi in x])
x0 = [1,5,5,1] # initial guesses

print('Initial SSE Objective: ' + str(objective(x0)))

# optimize
b = (1.0,5.0)
bnds = (b, b, b, b)
con1 = {'type': 'ineq', 'fun': constraint1} 
con2 = {'type': 'eq', 'fun': constraint2}
cons = ([con1,con2])
solution = minimize(objective,x0,method='SLSQP',\
                    bounds=bnds,constraints=cons)
x = solution.x
print('Final SSE Objective: ' + str(objective(x)))
print('x1 = ' + str(x[0])); print('x2 = ' + str(x[1]))
print('x3 = ' + str(x[2])); print('x4 = ' + str(x[3]))