sys = signal.StateSpace(A,B,C,D)
t,y,x = signal.lsim(sys,u,t)