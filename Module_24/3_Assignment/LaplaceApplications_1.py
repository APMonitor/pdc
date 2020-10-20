import matplotlib.pyplot as plt

plt.figure(1)
plt.plot([0,1,1.001,5,5.001,8],[0,0,3,3,0,0],'b-',linewidth=2)
plt.ylabel('y(t)')
plt.xlabel('time (t)')
plt.grid()
plt.savefig('fig1.png')

plt.figure(2)
plt.plot([0,2,4,6,8,10],[0,0,5,5,3,3],'r-',linewidth=2)
plt.ylabel('y(t)')
plt.xlabel('time (t)')
plt.grid()
plt.savefig('fig2.png')

plt.figure(3)
plt.plot([0,1,1.0001,4,4.0001,6],[0,0,-4,-4,2,8],'g-',linewidth=2)
plt.ylabel('y(t)')
plt.xlabel('time (t)')
plt.grid()
plt.savefig('fig3.png')
plt.show()