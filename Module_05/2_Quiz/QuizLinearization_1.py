# analytic solution with Python
import sympy as sp
# define symbols
y,u,d = sp.symbols(['y','u','d'])
# define equation
dydt = 3*y**3-(u**2-sp.sin(u))**(1/3)+sp.log(d)
# partial derivative with respect to u
beta = sp.diff(dydt,u)
# evaluate at steady state condition
print(beta.subs(u,4).evalf())