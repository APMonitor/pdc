from gekko import GEKKO
m = GEKKO(remote=False)
c = [100, 125]
A = [[3, 6], [8, 4]]
b = [30, 44]
x = m.qobj(c,otype='max')
m.axb(A,b,x=x,etype='<')
x[0].lower=0; x[0].upper=5
x[1].lower=0; x[1].upper=4
m.options.solver = 1
m.solve(disp=True)
print ('Product 1 (x1): ' + str(x[0].value[0]))
print ('Product 2 (x2): ' + str(x[1].value[0]))
print ('Profit        : ' + str(m.options.objfcnval))