def eulerstep(t, x, h):
    return x+h*ydot(t,x)

def ydot(t, x):
    g, L = 9.81, 2
    x_ = x[1]
    y_ = -(g/L)*sin(x[0])
    return [x_, y_]

h = 0.01

for i in range(1000):
    a, b = eulerstep(, h)