# numeric solution
from scipy.misc import derivative
m = 700.0   # kg
Cd = 0.24
rho = 1.225 # kg/m^3
A = 5.0     # m^2
Fp = 30.0   # N/%pedal
u = 40.0    # % pedal
v = 50.0    # km/hr (change this for SS condition)
def fv(v):
    return Fp*u/m - rho*A*Cd*v**2/(2*m)
def fu(u):
    return Fp*u/m - rho*A*Cd*v**2/(2*m)

print('Approximate Partial Derivatives')
print(derivative(fv,v,dx=1e-4))
print(derivative(fu,u,dx=1e-4))

print('Exact Partial Derivatives')
print(-A*Cd*rho*v/m) # exact d(f(u,v))/dv
print(Fp/m) # exact d(f(u,v))/du