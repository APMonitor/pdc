# analytic solution
import sympy as sp
sp.init_printing()
# define symbols
v,u = sp.symbols(['v','u'])
Fp,rho,Cd,A,m = sp.symbols(['Fp','rho','Cd','A','m'])
# define equation
eqn = Fp*u/m - rho*A*Cd*v**2/(2*m)

print(sp.diff(eqn,v))
print(sp.diff(eqn,u))