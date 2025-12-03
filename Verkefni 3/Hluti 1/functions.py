import numpy as np

def RKsolverLotkaVolterra(y0, T, n, f):

    y = np.zeros((n + 1, len(y0)))
    y[0, :] = y0
    h = T / n

    for i in range(n):
        k1 = f(y[i, :])
        k2 = f(y[i, :] + h/2 * k1)
        k3 = f(y[i, :] + h/2 * k2)
        k4 = f(y[i, :] + h * k3)

        y[i + 1, :] = y[i, :] + h/6 * (k1 + 2*k2 + 2*k3 + k4)

    return y


def ydot(yi, g=9.81, L=2):
    return [yi[1], (-g/L)*m.sin(yi[0])]

def eulerstep(yi, h, func):
    return [x + h*func(yi)[i] for i,x in enumerate(yi)]

def vtk(y0,T,n):

    y = [y0]
    h = T/n

    for i in range(n-1):
        y.append(eulerstep(y[i], h, ydot))

    theta = []
    omega = []

    for x in y:
        theta.append(x[0])
        omega.append(x[1])

    return 