import numpy as np
from numpy import linalg as la
import math as m

# Fastar #
v = 1*10^-3
r = 5*10^-2
L = 100
G = (m.pi*(r^4))/(8*v*L)
p1 = 4.2 * (10^6)
Q_b = 7

# Skilgreining á fyljunum a og b fyrir ax = b
A = np.matrix('3 1 1 0 0; 1 2 0 1 0; 1 0 -4 1 2; 0 3 3 -8 2; 0 0 6 2 -11')
B = np.matrix(f'{p1};{-Q_b/G}; 0; 0; 0')

# Nota linalg til að leysa fyrir x
x = la.solve(A,B)


