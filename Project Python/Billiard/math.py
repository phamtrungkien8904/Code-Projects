import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

a = [1,2,3]
b = [4,5,6]

u = np.zeros((3,2))
u[2,1] = 1

c = np.dot(a,b)
d = np.cross(a,b)

norm_d = np.linalg.norm(d)

print(c)

print(d)

print(norm_d)

print(np.sqrt(3**2 + 6**2 + (-3)**2))

print(u[2])

print(2*[1,2,3])