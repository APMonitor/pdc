# Stability Analysis
# YouTube: https://youtu.be/Y2BxAQxa0Vo
# thanks to Nikos Papadakis for the root locus slider bar
import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons

# open loop
num = [4.0]
den = [1.0,6.0,11.0,6.0]
def dcl(K):
    return [1.0,6.0,11.0,4.0*K+6.0]

# root locus plot
n = 10000 # number of points to plot
nr = len(den)-1 # number of roots
rs = np.zeros((n,2*nr))   # store results
Kc1 = -2.0
Kc2 = 18.0
Kc = np.linspace(Kc1,Kc2,n)  # Kc values
for i in range(n):        # cycle through n times
    roots = np.roots(dcl(Kc[i]))
    for j in range(nr):   # store roots
        rs[i,j] = roots[j].real # store real
        rs[i,j+nr] = roots[j].imag # store imaginary

# create the image
fig, ax = plt.subplots()
plt.subplots_adjust(left=0.10, bottom=0.25)
ls = []
for i in range(nr):
    plt.plot(rs[:,i],rs[:,i+nr],'r.',markersize=2)
    # this handle is required to update the plot
    if math.isclose(rs[0,i+nr],0.0):
        lbl = f'{rs[0,i]:0.2f}'
    else:
        lbl = f'{rs[0,i]:0.2f}, {rs[0,i+nr]:0.2f}i'
    l, = plt.plot(rs[0,i],rs[0,i+nr], 'ks', markersize=5,label=lbl)
    ls.append(l)  
leg = plt.legend(loc='best')
plt.xlabel('Root (real)')
plt.ylabel('Root (imag)')
plt.grid(b=True, which='major', color='b', linestyle='-',alpha=0.5)
plt.grid(b=True, which='minor', color='r', linestyle='--',alpha=0.5)

plt.xlim([-4.0,0.5])
#plt.ylim([-4.0,4.0])

# slider creation
axcolor = 'lightgoldenrodyellow'
axKc = plt.axes([0.10, 0.1, 0.80, 0.03], facecolor=axcolor)
sKc = Slider(axKc, 'Kc', Kc1, Kc2, valinit=0, valstep=0.1)

def update(val):
    Kc_val= sKc.val
    indx = (np.abs(Kc-Kc_val)).argmin()
    for i in range(nr):
        ls[i].set_ydata(rs[indx,i+nr])
        ls[i].set_xdata(rs[indx,i])
        if math.isclose(rs[indx,i+nr],0.0):
            lbl = f'{rs[indx,i]:0.2f}'
        else:
            lbl = f'{rs[indx,i]:0.2f}, {rs[indx,i+nr]:0.2f}i'
        leg.texts[i].set_text(lbl)
    fig.canvas.draw_idle()
sKc.on_changed(update)

resetax = plt.axes([0.8, 0.025, 0.1, 0.04])
button = Button(resetax, 'Reset', color=axcolor, hovercolor='0.975')

def reset(event):
    sKc.reset()
button.on_clicked(reset)

plt.show()