import numpy
import matplotlib as plt
import newton
import f
import Df

TOL = 10**(-14)

def make_grid(R_low, R_high, I_low, I_high, N):
    R = numpy.linspace(R_low, R_high, N)
    I = numpy.linspace(I_low, I_high, N)
    grid = []
    for i in R:
        grid.append([])
        for j in I:
            grid[-1].append(i+j*1j)
    return grid

grid = make_grid(-8, -6, -1, 1, 400)

results = []
for x in grid:
    results.append([])
    for y in x:
        results[-1].append(newton.newton(y, TOL, f.f, Df.Df))

results = [round(x, 5) for x in results]
