def eulerstep(t, x, h):
    return x+h*ydot(t,x)
def ydot(t, x):
    g, L = 9.81, 2
    return [x2, -(g/L)*sin(x1)]

h = 0.01