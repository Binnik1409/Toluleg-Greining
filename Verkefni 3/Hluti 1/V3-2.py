import math as m

def eulerstep(t, x, h):
    return [j+h*i for j,i in zip(x,ydot(t,x))]

def ydot(t, x):
    g, L = 9.81, 2
    x_ = x[1]
    y_ = -(g/L)*m.sin(x[0])
    return [x_, y_]

n = 10
t = 1
h = t/n
x = [20, 0]

for i in range(n):
    x = eulerstep(t, x, h)
    print(x)