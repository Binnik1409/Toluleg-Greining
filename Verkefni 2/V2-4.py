import numpy as np
from numpy import linalg as LA
from functions import newtonmult

def F(x):
    q1A, qAB, qAC, qBD, qCD, qCE, qDE, qE0 = x
    Fx = np.zeros(8)
    Fx[0] = q1A - qAB - qAC
    Fx[1] = qAB - qBD + QB
    Fx[2] = qAC - qCD - qCE
    Fx[3] = qBD + qCD - qDE
    Fx[4] = qCE + qDE - qE0
    Fx[5] = (qAB * abs(qAB) - qAC * abs(qAC) + qBD * abs(qBD) - qCD * abs(qCD))
    Fx[6] = (qCD * abs(qCD) - 0.5 * qCE * abs(qCE)) + 1.5 * qDE * abs(qDE)
    Fx[7] = eih + q1A * abs(q1A) + qAC * abs(qAC) + 0.5 * qCE * abs(qCE) + qE0 * abs(qE0)
    
    return Fx

def DF(x):
    q1A, qAB, qAC, qBD, qCD, qCE, qDE, qE0 = x

    J = np.zeros((8, 8))

    J[0, 0] =  1.0
    J[0, 1] = -1.0
    J[0, 2] = -1.0
    J[1, 1] =  1.0
    J[1, 3] = -1.0
    J[2, 2] =  1.0
    J[2, 4] = -1.0
    J[2, 5] = -1.0
    J[3, 3] =  1.0
    J[3, 4] =  1.0
    J[3, 6] = -1.0
    J[4, 5] =  1.0
    J[4, 6] =  1.0
    J[4, 7] = -1.0
    J[5, 1] =  2.0 * abs(qAB)
    J[5, 2] = -2.0 * abs(qAC)
    J[5, 3] =  2.0 * abs(qBD)
    J[5, 4] = -2.0 * abs(qCD)
    J[6, 4] =  2.0 * abs(qCD)
    J[6, 5] = -1.0 * abs(qCE)
    J[6, 6] =  3.0 * abs(qDE)
    J[7, 0] = 2.0 * abs(q1A)
    J[7, 2] = 2.0 * abs(qAC)
    J[7, 5] = 1.0 * abs(qCE)
    J[7, 7] = 2.0 * abs(qE0)

    return J

QB = 7.0
p0 = 0.0
p1 = 4.2*10**6
K  = 1.62*10**8
eih = (p0 - p1) / K

x = ["q1A", "qAB", "qAC", "qBD", "qCD", "qCE", "qDE", "qE0"]
x0 = np.array([1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0])
tol = 1*10**-8
sol = newtonmult(x0, tol, F, DF)
for i,j in enumerate(x):
    print(j,": ", sol[i], sep="")