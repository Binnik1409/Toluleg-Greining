import numpy as np
from numpy import linalg as la
import math as m

# Fastar #
v = 1*10^-3
r = 5*10^-2
L = 100
G = (m.pi*(r^4))/(8*v*L)
p1 = 4.2 * (10^6)
p0 = 0
Q_b = 7

# Skilgreining á fyljunum a og b fyrir ax = b
A = np.matrix('3 1 1 0 0; 1 2 0 1 0; 1 0 -4 1 2; 0 3 3 -8 2; 0 0 6 2 -11')
B = np.matrix(f'{p1};{-Q_b/G}; 0; 0; 0')

# Nota linalg til að leysa fyrir x
x = la.solve(A,B)

# setja upp gildin í poisulles jöfnuni til að reikna flæði í rörum milli punkta
poisuilles_gildi = [
    (G,   p1,  x[0]),       # q_1A
    (G,   x[0], x[1]),      # q_AB
    (G,   x[0], x[2]),      # q_AC
    (G,   x[1], x[3]),      # q_BD
    (G,   x[2], x[3]),      # q_CD
    (G,   x[2], x[4]),      # q_CE
    ((2/3)*G, x[3], x[4]),  # q_DE
    (G,   x[4], p0)         # q_E0 
]

# listi sem inniheldur reiknuð gildi úr poisulles jöfnuni 
flow = [g * (i - j) for g, i, j in poisuilles_gildi] #[q_1A, q_AB, q_AC, q_BD, q_CD, q_CE, q_DE, q_E0]
r = '  '.join(map(str, flow)).replace("[[","").replace("]]","")

# Print
print('q_1A         q_AB         q_AC         q_BD         q_CD         q_CE         q_DE         q_E0')
print(r)