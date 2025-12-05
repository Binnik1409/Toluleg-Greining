import matplotlib.pyplot as plt
import math as m
import functions as f

# Fastar
N = [200, 400, 800, 1600, 3200, 6400]
T = 20
h = [T/n for n in N]
y0 = [m.pi-0.2,m.pi,0,0]

sol = []
for n in N:
    res = f.RKsolver_Y4(y0, T, n, f.f2,'y')
    sol.append(res)

res_ref = f.RKsolver_Y4(y0, T, 12800, f.f2,'y')

errors = []
for res in sol:        
    sum = 0
    for i in range(len(res_ref)):
        sum += (res[i] - res_ref[i])**2
    errors.append(m.sqrt(sum))


plt.figure()
plt.scatter(N, errors, marker='o', label="RK-error")
plt.plot(N, errors)
plt.scatter(N, h, marker='o', label="h^4")
plt.xlabel("h = T/n")
plt.plot(N, h)
plt.ylabel("skekkja")
plt.legend()
plt.grid(True, which="both")
plt.show()

