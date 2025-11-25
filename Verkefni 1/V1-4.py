import numpy as np
import matplotlib.pyplot as plt
import functions as f

ROUND = 2
TOL = 10**(-3)

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
        results[-1].append(f.newton(y, TOL, f.f, f.Df))

four_solutions = []

for x in results:
    for y in x:
        four_solutions.append(np.round(y, ROUND))


four_solutions = list(set(four_solutions))


result_colors = []

for x in results:
    result_colors.append([])
    for y in x:
        y=np.round(y, ROUND)
        if y in four_solutions:
            result_colors[-1].append(four_solutions.index(y))
        else:
            print("Got", y, "which is not in four_solutions")
            exit("Error: Result not one of four")
            
groups = []
for i,x in enumerate(result_colors):
    for j,y in enumerate(x):
        while len(groups) < y+1:
            groups.append([])
        groups[y].append((grid[i][j].real, grid[i][j].imag))
colors = ["blue", "green", "red", "yellow"]


plt.figure()
for i,x in enumerate(groups):
    real = [j[0] for j in x]
    imag = [j[1] for j in x]
    plt.scatter(real, imag, s=10, marker='o', linewidths=0, color=colors[i], label=four_solutions[i])
plt.gca().set_aspect('equal', adjustable='box')
plt.axis('on')
plt.grid(False)
plt.legend()
plt.show()