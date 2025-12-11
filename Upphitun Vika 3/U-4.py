import numpy as np
import matplotlib.pyplot as plt



n = 50
L = np.pi/2
h = L/(n-1)

x = np.linspace(0, np.pi/2, n)


alpha = -2 + h**2


diag1 = np.diag([1 for i in range(n-1)], -1)
diag2 = np.diag([1 for i in range(n-1)], 1)
diag3 = np.diag([alpha for i in range(n)])
A = diag1 + diag2 + diag3
A[0][0] = -3-2*h
A[0][1] = 4
A[0][2] = -1
A[-1][-1] = -3-4*h
A[-1][-2] = 4
A[-1][-3] = -1
print(A)

b = np.zeros(n)
b[0] = 0
b[-1] = -2*h
#print(b)

sol = np.linalg.solve(A, b)
#print(sol)
y = np.sin(x) + np.cos(x)

plt.plot(x, sol)

plt.plot(x, y)

plt.legend(["Nálgun", "Rétt lausn"])

plt.show()