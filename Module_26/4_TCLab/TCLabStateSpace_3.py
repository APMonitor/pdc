# state space simulation
ss = GEKKO()
x,y,u = ss.state_space(Am,Bm,Cm,D=None)
u[0].value = data['Q1'].values
u[1].value = data['Q2'].values
ss.time = data['Time'].values
ss.options.IMODE = 7
ss.solve(disp=False)