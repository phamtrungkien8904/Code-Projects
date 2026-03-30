import numpy as np
import matplotlib.pyplot as plt 

data = np.loadtxt("data.csv", delimiter=",", skiprows=1)
x = data[:, 0]
y = data[:, 1]

plt.plot(x, y, marker='o', linestyle='-', color='b')
plt.title("Sample Data Plot")
plt.xlabel("X-axis")
plt.ylabel("Y-axis")
plt.show()