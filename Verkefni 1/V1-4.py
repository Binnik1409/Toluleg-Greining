import numpy as np
import matplotlib.pyplot as plt
import functions as f


ACCURACY = 2 # fjöldi aukastafna
GRID_SIZE = 400 # fjöldi punkta í grid
                #Hærri tala = hærri upplausn og lengri tími

ROUND = ACCURACY
TOL = 10**(-ACCURACY-1)



def make_grid(R_low, R_high, I_low, I_high, N):
    R = np.linspace(R_low, R_high, N)
    I = np.linspace(I_low, I_high, N)
    grid = []
    for i in R:
        grid.append([])
        for j in I:
            grid[-1].append(i+j*1j)
    return grid
#Býr til 400x400 grid af punktum


grid = make_grid(-8, -6, -1, 1, GRID_SIZE)

results = []
for x in grid:
    results.append([])
    for y in x:
        results[-1].append(f.newton(y, TOL, f.f, f.Df))
#Notar newton aðferðina

four_solutions = []

for x in results:
    for y in x:
        four_solutions.append(np.round(y, ROUND))
#Setur allar lausnir í einn lista

four_solutions = list(set(four_solutions))
#Tekur út endurtektir af lausnum og endar í fjórum


for i, x in enumerate(four_solutions):
    print("Lausn", (str(i+1) + ":"), x)
#Sýnir lausnir


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
#Gefur hverri staðsetningu í gridinu tölu á bilinu 0-3 eftir hvaða lausn upphafspunktur gefur
            
groups = []
for i,x in enumerate(result_colors):
    for j,y in enumerate(x):
        while len(groups) < y+1:
            groups.append([])
        groups[y].append((grid[i][j].real, grid[i][j].imag))
colors = ["blue", "green", "red", "black"]
#Skiptir upphafspunktum niður í hópa eftir hvaða lausn þeir gefa


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
#Plottar lausnir