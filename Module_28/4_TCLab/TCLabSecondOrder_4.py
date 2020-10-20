# 2nd order step response
def model(y0,t,M,Kp,taus,zeta):
    # y0 = initial y
    # t  = time
    # M  = magnitude of the step
    # Kp = gain
    # taus = second order time constant
    # zeta = damping factor (zeta>1 for overdamped)
    a = np.exp(-zeta*t/taus)
    b = np.sqrt(zeta**2-1.0)
    c = (t/taus)*b
    y = Kp * M * (1.0 - a * (np.cosh(c)+(zeta/b)*np.sinh(c))) + y0
    return y