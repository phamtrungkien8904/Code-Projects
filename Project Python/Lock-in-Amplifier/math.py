import numpy as np
import matplotlib.pyplot as plt


t_min = -10
t_max = 10
dt = 0.01
t = np.arange(t_min, t_max, dt)
y1 = 10*np.sin(2*t) + 0.5*np.sin(5*t) + 0.3*np.sin(10*t) + 0.1*np.sin(20*t) + 0.2*np.sin(50*t)+10
y2 = np.sin(2*t +np.pi/3)  
y3 = np.sum(y1 * y2) * dt/(t_max - t_min)
print("Phase of Signal-Ref:", np.angle(y3))
print("Amplitude of Signal:", y3*2)


plt.plot(t, y1, label='Signal')
plt.plot(t, y2, label='Reference')
plt.legend()
plt.title('Signal and Reference')
plt.xlabel('x')
plt.ylabel('sinc(x)')
plt.show()