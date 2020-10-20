# state space simulation with scipy
sys = signal.StateSpace(Am,Bm,Cm,Dm)
tsys = data['Time'].values
Qsys = np.vstack((data['Q1'].values,data['Q2'].values))
Qsys = Qsys.T
tsys,ysys,xsys = signal.lsim(sys,Qsys,tsys)