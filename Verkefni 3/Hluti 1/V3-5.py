import math as m
import numpy as np
from functions import RKsolverLotkaVolterra

def f(y):
    x, z = y
    g, L = 9.81, 2
    dxdt = z
    dzdt = -(g/L)*m.sin(x)
    return np.array([dxdt, dzdt])


T = 20
n = 500

y0 = [m.pi/12, 0]
solution_1 = RKsolverLotkaVolterra(y0, T, n, f)

y0 = [m.pi/2, 0]
solution_2 = RKsolverLotkaVolterra(y0, T, n, f)

print(solution_2)
print()