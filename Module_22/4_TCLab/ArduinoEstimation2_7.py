import numpy as np
from scipy.optimize import curve_fit
import uncertainties as unc
import matplotlib.pyplot as plt
import uncertainties.unumpy as unp
from scipy.integrate import odeint
import pandas as pd
from scipy import stats

# calculate lower and upper prediction bands
def predband(x, xd, yd, f_vars, conf=0.95):
    """
    Code adapted from Rodrigo Nemmen's post:
    https://astropython.blogspot.com.ar/2011/12/calculating-prediction-band-
    of-linear.html

    Calculates the prediction band of the regression model at the
    desired confidence level.

    Clarification of the difference between confidence and prediction bands:

    "The prediction bands are further from the best-fit line than the
    confidence bands, a lot further if you have many data points. The 95%
    prediction band is the area in which you expect 95% of all data points
    to fall. In contrast, the 95% confidence band is the area that has a
    95% chance of containing the true regression line."
    (from https://www.graphpad.com/guides/prism/6/curve-fitting/index.htm?
    reg_graphing_tips_linear_regressio.htm)

    Arguments:
    - x: array with x values to calculate the confidence band.
    - xd, yd: data arrays.
    - a, b, c: linear fit parameters.
    - conf: desired confidence level, by default 0.95 (2 sigma)

    References:
    1. https://www.JerryDallal.com/LHSP/slr.htm, Introduction to Simple Linear
    Regression, Gerard E. Dallal, Ph.D.
    """
    alpha = 1. - conf    # Significance
    N = xd.size          # data sample size
    var_n = len(f_vars)  # Number of variables used by the fitted function.
    # Quantile of Student's t distribution for p=(1 - alpha/2)
    q = stats.t.ppf(1. - alpha / 2., N - var_n)
    # Std. deviation of an individual measurement (Bevington, eq. 6.15)
    se = np.sqrt(1. / (N - var_n) * np.sum((yd - simulate(xd, *f_vars)) ** 2))
    # Auxiliary definitions
    sx = (x - xd.mean()) ** 2
    sxd = np.sum((xd - xd.mean()) ** 2)
    # Predicted values (best-fit model)
    yp = simulate(x, *f_vars)
    # Prediction band
    dy = q * se * np.sqrt(1. + (1. / N) + (sx / sxd))
    # Upper & lower prediction bands.
    lpb, upb = yp - dy, yp + dy
    return lpb, upb

# generate data file from TCLab or get sample data file from:
#  https://apmonitor.com/pdc/index.php/Main/ArduinoEstimation2
# Import data file
# Column 1 = time (t)
# Column 2 = input (u)
# Column 3 = output (yp)
data = np.loadtxt('data.txt',delimiter=',',skiprows=1)
# extract data columns
t = data[:,0].T
Q1 = data[:,1].T
Q2 = data[:,2].T
T1meas = data[:,3].T
T2meas = data[:,4].T
ind = np.linspace(0,np.size(t),np.size(t))

# number of time points
ns = len(t)

# define energy balance model
def heat(x,t,Q1,Q2,p):
    # Optimized parameters
    U,alpha1,alpha2 = p

    # Parameters
    Ta = 23 + 273.15   # K
    m = 4.0/1000.0     # kg
    Cp = 0.5 * 1000.0  # J/kg-K    
    A = 10.0 / 100.0**2 # Area in m^2
    As = 2.0 / 100.0**2 # Area in m^2
    eps = 0.9          # Emissivity
    sigma = 5.67e-8    # Stefan-Boltzman

    # Temperature States 
    T1 = x[0] + 273.15
    T2 = x[1] + 273.15

    # Heat Transfer Exchange Between 1 and 2
    conv12 = U*As*(T2-T1)
    rad12  = eps*sigma*As * (T2**4 - T1**4)

    # Nonlinear Energy Balances
    dT1dt = (1.0/(m*Cp))*(U*A*(Ta-T1) \
            + eps * sigma * A * (Ta**4 - T1**4) \
            + conv12 + rad12 \
            + alpha1*Q1)
    dT2dt = (1.0/(m*Cp))*(U*A*(Ta-T2) \
            + eps * sigma * A * (Ta**4 - T2**4) \
            - conv12 - rad12 \
            + alpha2*Q2)

    return [dT1dt,dT2dt]

def simulate(tm,U,alpha1,alpha2):
    T = np.zeros((len(t),2))
    T[0,0] = T1meas[0]
    T[0,1] = T2meas[0]    
    T0 = T[0]
    p = (U,alpha1,alpha2)
    for i in range(len(t)-1):
        ts = [t[i],t[i+1]]
        y = odeint(heat,T0,ts,args=(Q1[i],Q2[i],p))
        T0 = y[-1]
        T[i+1] = T0
    z = np.empty((len(t)*2))
    z[0:len(t)] = T[:,0]
    z[len(t):] = T[:,1]
    return z

def simulate2(p):
    T = np.zeros((len(t),2))
    T[0,0] = T1meas[0]
    T[0,1] = T2meas[0]    
    T0 = T[0]
    for i in range(len(t)-1):
        ts = [t[i],t[i+1]]
        y = odeint(heat,T0,ts,args=(Q1[i],Q2[i],p))
        T0 = y[-1]
        T[i+1] = T0
    return T

# Parameter initial guess
U = 10.0           # Heat transfer coefficient (W/m^2-K)
alpha1 = 0.0100    # Heat gain 1 (W/%)
alpha2 = 0.0075    # Heat gain 2 (W/%)
pinit = [U,alpha1,alpha2]

x = []
y = np.empty((len(t)*2))
y[0:len(t)] = T1meas
y[len(t):] = T2meas

popt, pcov = curve_fit(simulate, x, y)

Uu, alpha1u, alpha2u = unc.correlated_values(popt, pcov)

# create prediction band
lpb, upb = predband(y, y, y, popt, conf=0.95)
lpb1 = np.empty((len(t)))
lpb2 = np.empty((len(t)))
upb1 = np.empty((len(t)))
upb2 = np.empty((len(t)))
lpb1[0:len(t)] = lpb[0:len(t)]
lpb2[0:len(t)] = lpb[len(t):]
upb1[0:len(t)] = upb[0:len(t)]
upb2[0:len(t)] = upb[len(t):]

# optimized parameter values with uncertainties
print('Optimal Parameters with Uncertanty Range')
print('U: ' + str(Uu))
print('alpha1: ' + str(alpha1u))
print('alpha2: ' + str(alpha2u))

# calculate model with updated parameters
Ti  = simulate2(pinit)
Tp  = simulate2(popt)

# Plot results
plt.figure(1)

plt.subplot(3,1,1)
plt.plot(t/60.0,Ti[:,0],'y:',label=r'$T_1$ initial')
plt.plot(t/60.0,T1meas,'b-',label=r'$T_1$ measured')
plt.plot(t/60.0,Tp[:,0],'r--',label=r'$T_1$ optimized')
plt.plot(t/60.0,lpb1,'k:',label=r'$T_1$ prediction band')
plt.plot(t/60.0,upb1,'k:')

plt.ylabel('Temperature (degC)')
plt.legend(loc='best')

plt.subplot(3,1,2)
plt.plot(t/60.0,Ti[:,1],'y:',label=r'$T_2$ initial')
plt.plot(t/60.0,T2meas,'b-',label=r'$T_2$ measured')
plt.plot(t/60.0,Tp[:,1],'r--',label=r'$T_2$ optimized')
plt.plot(t/60.0,lpb2,'k:',label=r'$T_2$ prediction band')
plt.plot(t/60.0,upb2,'k:')
plt.ylabel('Temperature (degC)')
plt.legend(loc='best')

plt.subplot(3,1,3)
plt.plot(t/60.0,Q1,'g-',label=r'$Q_1$')
plt.plot(t/60.0,Q2,'k--',label=r'$Q_2$')
plt.ylabel('Heater Output')
plt.legend(loc='best')

plt.xlabel('Time (min)')
plt.show()