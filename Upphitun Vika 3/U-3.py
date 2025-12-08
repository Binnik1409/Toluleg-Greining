import functions as f
import numpy as np
import matplotlib.pyplot as plt

n = 20
L = np.pi/2
h = L/(n-1)


x = np.linspace(0, np.pi/2, n)

alpha = 1
beta = -2 + h**2

matrix_a = f.create_matrix_A(n, alpha, beta)
matrix_a[0] = np.array([-3,4,-1] + [0]*(n-3))
matrix_a[-1] = np.array([0]*(n-3) + [1,-4,3])
vector_b = np.zeros(n)
vector_b[0] = 2*h
vector_b[-1] = 6*h

sol = np.linalg.solve(matrix_a, vector_b)

ref_sol = -3 * np.cos(x) + np.sin(x)

plt.plot(x, sol, marker='o', label='Numerical Solution')
plt.plot(x, ref_sol, label='Reference Solution', linestyle='--')
plt.title('Numerical Solution of BVP')
plt.xlabel('x')
plt.ylabel('y')
plt.legend()
plt.grid()
plt.show()