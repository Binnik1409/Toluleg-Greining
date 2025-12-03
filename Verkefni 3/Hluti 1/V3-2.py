import numpy as np
import math as m
import matplotlib.pyplot as plt

def ydot(yi, g=9.81, L=2):
    return [yi[1], (-g/L)*m.sin(yi[0])]

def eulerstep(yi, h, func):
    return [x + h*func(yi)[i] for i,x in enumerate(yi)]



y0 = [1, 1] #!!!!!!!!!!!!!!!!

y = [y0]
n = 100
T = 3
h = T/n

for i in range(n):
    y.append(eulerstep(y[i], h, ydot))

theta = []
omega = []

for x in y:
    theta.append(x[0])
    omega.append(x[1])

x = np.linspace(0, T, n+1)

plt.plot(x, theta)
plt.show()