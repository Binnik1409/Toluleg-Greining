import functions as f
import numpy as np
import matplotlib.pyplot as plt

y0 = 1
yn = -5
n = 20
L = np.pi/2
h = L/(n-1)

x = np.linspace(0, np.pi/2, n)

alpha = 1
beta = -2 + h**2

matrix_a = f.create_matrix_A(n, alpha, beta)
vector_b = np.zeros(n)
vector_b[0] = -3*y0/2*h
vector_b[-1] = -3*yn/-2*h

sol = np.linalg.solve(matrix_a, vector_b)

ref_sol = np.cos(x) - 5 * np.sin(x)

plt.plot(x, sol, marker='o', label='Numerical Solution')
plt.plot(x, ref_sol, label='Reference Solution', linestyle='--')
plt.title('Numerical Solution of BVP')
plt.xlabel('x')
plt.ylabel('y')
plt.legend()
plt.grid()
plt.show()