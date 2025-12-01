import math as m

def eulerstep(t, x, h):
    return [j+h*i for j,i in zip(x,ydot(t,x))]

def ydot(t, x):
    g, L = 9.81, 2
    x_ = x[1]
    y_ = -(g/L)*m.sin(x[0])
    return [x_, y_]

n = 100
T = 3
h = T/n
x = [m.radians(20), 0]

t = 0
for i in range(n):
    x = eulerstep(t, x, h)
    t += h
    print(m.degrees(x[0]), x[1])