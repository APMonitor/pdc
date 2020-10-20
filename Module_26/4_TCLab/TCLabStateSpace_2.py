Am = np.zeros((4,4))
Bm = np.zeros((4,2))
Cm = np.zeros((2,4))
Dm = np.zeros((2,2))

T0 = Ta
c1 = U.value[0]*A
c2 = 4*eps*sigma*A*T0**3
c3 = Us.value[0]*As
c4 = 4*eps*sigma*As*T0**3
c5 = mass*Cp
c6 = 1/tau.value[0]

Am[0,0] = -(c1+c2+c3+c4)/c5
Am[0,1] = (c3+c4)/c5

Am[1,0] = 
Am[1,1] = 

Am[2,0] = c6
Am[2,2] = 

Am[3,1] = 
Am[3,3] = -c6

Bm[0,0] = alpha1.value[0]/c5
Bm[1,1] = 

Cm[0,2] = 1
Cm[1,3] = 