ss = GEKKO()
x,y,u = ss.state_space(A,B,C,D=None)
ss.options.IMODE = 7
ss.solve(disp=False)