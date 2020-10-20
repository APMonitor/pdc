# solve with GEKKO and sparse matrices
import numpy as np
from gekko import GEKKO
m = GEKKO(remote=False)
# [[row indices],[column indices],[values]]
A_sparse = [[1,1,2,2],[1,2,1,2],[3,6,8,4]]
# [[row indices],[values]]
b_sparse = [[1,2],[30,44]]
x = m.axb(A_sparse,b_sparse,etype='<',sparse=True)
# [[row indices],[values]]
c_sparse = [[1,2],[100,125]]
m.qobj(c_sparse,x=x,otype='max',sparse=True)
x[0].lower=0; x[0].upper=5
x[1].lower=0; x[1].upper=4
m.solve(disp=True)
print(m.options.OBJFCNVAL)
print('x: ' + str(x))