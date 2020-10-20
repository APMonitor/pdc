import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

# open loop
num = [4.0]
den = [1.0,6.0,11.0,6.0]
sys = signal.TransferFunction(num, den)
t1,y1 = signal.step(sys)

# closed loop
Kc = 1.0
num = [4.0*Kc]
den = [1.0,6.0,11.0,4.0*Kc+6.0]
sys2 = signal.TransferFunction(num, den)
t2,y2 = signal.step(sys2)

plt.figure(1)
plt.subplot(2,1,1)
plt.plot(t1,y1,'k-')
plt.legend(['Open Loop'],loc='best')

plt.subplot(2,1,2)
plt.plot(t2,y2,'r--')
plt.legend(['Closed Loop'],loc='best')
plt.xlabel('Time')

# root locus plot
n = 1000  # number of points to plot
nr = 3    # number of roots
rs = np.zeros((n,2*nr))   # store results
Kc = np.logspace(-2,2,n)  # Kc values
for i in range(n):        # cycle through n times
    den = [1.0,6.0,11.0,4.0*Kc[i]+6.0] # polynomial
    roots = np.roots(den) # find roots
    for j in range(nr):   # store roots
        rs[i,j] = roots[j].real # store real
        rs[i,j+nr] = roots[j].imag # store imaginary
plt.figure(2)
plt.subplot(2,1,1)
plt.xlabel('Root (real)')
plt.ylabel('Root (imag)')
plt.grid(b=True, which='major', color='b', linestyle='-')
plt.grid(b=True, which='minor', color='r', linestyle='--')
for i in range(nr):
    plt.plot(rs[:,i],rs[:,i+nr],'.')
plt.subplot(2,1,2)
plt.plot([Kc[0],Kc[-1]],[0,0],'k-')
for i in range(3):
    plt.plot(Kc,rs[:,i],'.')
plt.ylabel('Root (real part)')
plt.xlabel('Controller Gain (Kc)')

# bode plot
w,mag,phase = signal.bode(sys)
# compute the gain margin
mag_f = interp1d(phase, mag)
mag_f(-180)  # magnitude at -180 degrees
AR = 10**(mag_f(-180)/20.0)
print('Gain Margin : {}'.format(1.0/AR))

plt.figure(3)

plt.subplot(2,1,2) # bottom plot
plt.semilogx(w,phase,'k-',linewidth=3)
plt.grid(b=True, which='major', color='grey', alpha=0.3, linestyle='-')
plt.grid(b=True, which='minor', color='grey', alpha=0.3, linestyle='--')

# show graphical gain margin calc on plot
w_i = interp1d(phase,w)
mag_i = interp1d(w,mag)
wcr = w_i(-180.0)
# gain ratio 1: show freq that intersects at -180 phase
plt.semilogx([0.01,wcr],[-180,-180], 'k:', lw=3)
# gain ratio 2: show mag at that frequency
plt.semilogx([wcr,wcr],[-180,0], 'k:', lw=3)
plt.text(0.01,-170,f'Step 1: Freq={wcr:0.2f} at -180 deg Phase')

plt.ylabel('Phase')
plt.xlabel('Frequency')

plt.subplot(2,1,1) # top plot
plt.semilogx(w,mag,'k-',linewidth=3)
plt.grid(b=True, which='major', color='grey', alpha=0.3, linestyle='-')
plt.grid(b=True, which='minor', color='grey', alpha=0.3, linestyle='--')
plt.ylabel('Magnitude')

# gain ratio 3: 
plt.semilogx([wcr,wcr],[-50,mag_i(wcr)], 'k:', lw=3)
# gain ratio 4:
plt.semilogx([0.01,wcr],[mag_i(wcr),mag_i(wcr)], 'k:', lw=3)
plt.text(0.01,mag_i(wcr)-5,f'Step 2: Mag={mag_i(wcr):0.2f} at Freq={wcr:0.2f}')
AR = 10**(mag_i(wcr)/20.0)
plt.text(0.01,mag_i(wcr)-10,f'Step 3: Amp Ratio={AR:0.2f} ' + \
                            f'from {mag_i(wcr):0.2f} = ' + \
                            '20$\log_{10}(AR)$')
plt.text(0.01,mag_i(wcr)-15,f'Step 4: Gain Margin={1.0/AR:0.2f} ' + \
                            f'from 1/AR')


plt.show()