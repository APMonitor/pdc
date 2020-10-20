# simulate model with x=[Km,taum,thetam]
def sim_model(x):
    # input arguments
    Kp = x[0]
    taus = x[1]
    zeta = x[2]
    thetap = x[3]
    # storage for model values
    xm = np.zeros((ns,2))  # model
    # initial condition
    xm[0] = xp0
    # loop through time steps    
    for i in range(0,ns-1):
        ts = [t[i],t[i+1]]
        inputs = (uf,Kp,taus,zeta,thetap)
        # turn off warnings
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            # integrate SOPDT model
            x = odeint(sopdt,xm[i],ts,args=inputs)
        xm[i+1] = x[-1]
    y = xm[:,0]
    return y