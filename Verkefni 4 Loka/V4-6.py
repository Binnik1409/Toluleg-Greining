import functions as f
import numpy as np
import matplotlib.pyplot as plt

Lx = Ly = 10
delta = 0.1
P = 5
K = 1.68
H = 0.005
U = 20
n = 200
m = 200

results = []

for i in range(Lx-1):
    for j in range(i+1, Lx):
        L = j - i
        run = f.best_cpu_placement(L=L, POWER_START=i, POWER_END=j)
        results.append((np.mean(run), run, (i, j)))

    
best_result = min(results, key=lambda x: x[0])
plt.imshow(best_result[1], origin="lower", extent=[0, Lx, 0, Ly], aspect="auto")
plt.colorbar(label="Temperature (°C)")
plt.xlabel("x (cm)")
plt.ylabel("y (cm)")
plt.show()
print(f'Best power placement: {best_result[2]} with average temperature {best_result[0]} °C')

x = np.linspace(0, Lx, m)
y = np.linspace(0, Ly, n)
X, Y = np.meshgrid(x, y)

fig = plt.figure()
ax = fig.add_subplot(111, projection="3d")
ax.plot_surface(X, Y, best_result[1])                     
ax.set_xlabel("x (cm)")
ax.set_ylabel("y (cm)")
ax.set_zlabel("Temperature (°C)")
plt.show()