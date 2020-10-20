# solve with SciPy
from scipy.optimize import linprog
c = [-100, -125]
A = [[3, 6], [8, 4]]
b = [30, 44]
x0_bounds = (0, 5)
x1_bounds = (0, 4)
res = linprog(c, A_ub=A, b_ub=b, \
              bounds=(x0_bounds, x1_bounds),
              options={"disp": True})
print(res)