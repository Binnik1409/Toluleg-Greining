import numpy as np
import matplotlib as plt
import newton
import f
import Df

ROUND = 5
TOL = 10**(-14)

def make_grid(R_low, R_high, I_low, I_high, N):
    R = np.linspace(R_low, R_high, N)
    I = np.linspace(I_low, I_high, N)
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

all_results = []

for x in results:
    for y in x:
        all_results.append(np.round(y, ROUND))

print(len(all_results))
all_results = list(set(all_results))

print(len(all_results))

for item in all_results:
    print(item)