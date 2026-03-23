import matplotlib.pyplot as plt
print("Hello World!")

N = 20
k = [[i,i**2] for i in range(N)]
x = [i for i in range(N)]
y = [i**2 for i in x]
plt.plot(x,y,'o')
plt.show()

