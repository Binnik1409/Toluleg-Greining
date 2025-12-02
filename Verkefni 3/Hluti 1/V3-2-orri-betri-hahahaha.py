import math as m
import numpy as np

def eulerstep(y, h, f):
    return [y[0]+y[1]*h, f(y[0])]

def ydot(y):
    g, L = 9.81, 2
    return [y[1], -(g/L)*m.sin(y[0])]

T = 30
n = 500
h = T/n

y0 = [20]
w0 = [2]

y0.extend(np.zeros(n-1))
w0.extend(np.zeros(n-1))


y = np.matrix([y0, w0])

for i in range(n):
    y[:,i+1] = eulerstep(y[:,i], h, ydot)

np.plot([i for i in n], y[0])