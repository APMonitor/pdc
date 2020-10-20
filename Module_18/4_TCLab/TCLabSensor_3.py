def T(mV):
    return round(0.1*mV-50.0,1)

def mV(T):
    return round((T+50.0)*10.0,2)

print('mV signal at 25 degC: ' + str(mV(25)))
print('mV signal at 80 degC: ' + str(mV(80)))
print('T at 0.5V: ' + str(T(0.5*1000)))
print('T at 1.2V: ' + str(T(1.2*1000)))

print('Current temperature for T1 and T2 in Celsius and milliVolts')
import tclab
lab = tclab.TCLab()
T1 = lab.T1
T2 = lab.T2
T1mV = (T1+50.0)*10.0
T2mV = (T2+50.0)*10.0
print('T1: '+str(T1)+' degC')
print('T2: '+str(T2)+' degC')
print('T1: '+str(round(T1mV))+' mV')
print('T2: '+str(round(T2mV))+' mV')
lab.close()