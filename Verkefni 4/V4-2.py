
import numpy as np
from scipy.sparse import coo_matrix
from scipy.sparse.linalg import spsolve
import matplotlib.pyplot as plt

m, n = 10, 10
a, b, c, d = 0, 2, 0, 2
C, h = 1.68, 0.005
hx = (b - a) / (m - 1)
hy = (d - c) / (n - 1)

# six coefficients
alpha = 1 / (hy ** 2)
beta = 1 / (hx ** 2)
gamma = -2 / (hx ** 2) - 2 / (hy ** 2)
delta = C / (2 * hx)
epsilon = (2 * C) / hx
zeta = (3 * C) / (2 * hx) + h

# main diagonal
i = list(range(1, m * n + 1))
j = list(range(1, m * n + 1))
x = np.concatenate(([-3], gamma * np.ones(m - 2), [zeta]))
maindiag = np.concatenate((np.ones(m), np.tile(x, m - 2), np.ones(m)))

# upper diagonal one off
i += list(range(1, m * n))
j += list(range(2, m * n + 1))
x = np.concatenate(([4], beta * np.ones(m - 2), [0]))
upperdiag = np.concatenate((np.zeros(m), np.tile(x, m - 2), np.zeros(m - 1)))

# upper diagonal two off
i += list(range(1, m * n - 1))
j += list(range(3, m * n + 1))
x = np.concatenate(([-1], np.zeros(m - 1)))
upperdiag2 = np.concatenate((np.zeros(m), np.tile(x, m - 2), np.zeros(m - 2)))

# lower diagonal one off
i += list(range(2, m * n + 1))
j += list(range(1, m * n))
x = np.concatenate(([0], beta * np.ones(m - 2), [epsilon]))
lowerdiag = np.concatenate((np.zeros(m - 1), np.tile(x, m - 2), np.zeros(m)))

# lower diagonal two off
i += list(range(3, m * n + 1))
j += list(range(1, m * n - 1))
x = np.concatenate((np.zeros(m - 1), [delta]))
lowerdiag2 = np.concatenate((np.zeros(m - 2), np.tile(x, m - 2), np.zeros(m)))

# alpha diagonal left − m to the left of main diagonal, total length is mn−m
i += list(range(m + 1, m * n + 1))
j += list(range(1, m * n - m + 1))
x = np.concatenate(([0], alpha * np.ones(m - 2), [0]))
alphadiag1 = np.concatenate((np.tile(x, m - 2), np.zeros(m)))

# alpha diagonal right − m to the right of main diagonal, total length is mn−m
i += list(range(1, m * n - m + 1))
j += list(range(m + 1, m * n + 1))
x = np.concatenate(([0], alpha * np.ones(m - 2), [0]))
alphadiag2 = np.concatenate((np.zeros(m), np.tile(x, m - 2)))

# construct sparse matrix
values = np.concatenate([maindiag, upperdiag, upperdiag2, lowerdiag,
                         lowerdiag2, alphadiag1, alphadiag2])

Asparse = coo_matrix((values, (np.array(i) - 1, np.array(j) - 1)), shape=(m * n, m * n))


# Assuming m, n, h, and Asparse are defined previously

i = np.concatenate([np.arange(1, m+1), np.arange(2*m, (n-1)*m+1, m), np.arange((n-1)*m+1, n*m+1)]) - 1
j = np.zeros(i.shape, dtype=int)
values = np.concatenate([200 * np.ones(m), 30 * h * np.ones(n-2), 200 * np.ones(m)])

bsparse = coo_matrix((values, (i, j)), shape=(n*m, 1))

w = spsolve(Asparse, bsparse.toarray())

#plt.spy(Asparse)
#plt.show()

plt.imshow(w.reshape((n, m)), extent=(a, b, c, d), origin='lower')
plt.show()