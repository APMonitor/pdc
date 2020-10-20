import pandas as pd
import matplotlib.pyplot as plt

# pipeline data URL (don't need wget)
url = 'https://apmonitor.com/pdc/uploads/Main/pipeline_data.txt'

# import data with pandas
data = pd.read_csv(url)
time = 'Time (min)'
valve = 'Valve Position (% open)'
TC = 'Temperature (degC)'

# print temperature values
print(TC)
print(data[TC][0:5])
print('min: '+str(min(data[TC])))
print('max: '+str(max(data[TC])))

# plot data with pyplot
plt.figure()
plt.subplot(2,1,1)
plt.plot(data[time]/60.0,data[valve],'b--')
plt.ylabel(valve)

plt.subplot(2,1,2)
plt.plot(data[time]/60.0,data[TC],'r-')
plt.ylabel(TC)
plt.xlabel('Time (hr)')
plt.show()