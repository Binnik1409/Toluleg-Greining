import numpy as np
from numpy import linalg as LA

QB = 7.0
p0 = 0.0
p1 = 4.2e6
K  = 1.62e8   # your value
const_energy = (p0 - p1) / K   # ≈ -0.0259259...

def F(x):
    """
    x = [q1A, qAB, qAC, qBD, qCD, qCE, qDE, qE0]
    returns F(x) as an 8-vector
    """
    q1A, qAB, qAC, qBD, qCD, qCE, qDE, qE0 = x

    Fx = np.zeros(8)

    # 1) Node A
    Fx[0] = q1A - qAB - qAC

    # 2) Node B
    Fx[1] = qAB - qBD + QB

    # 3) Node C
    Fx[2] = qAC - qCD - qCE

    # 4) Node D
    Fx[3] = qBD + qCD - qDE

    # 5) Node E
    Fx[4] = qCE + qDE - qE0

    # 6) Loop 1: qAB|qAB| - qAC|qAC| + qBD|qBD| - qCD|qCD|
    Fx[5] = (
        qAB * abs(qAB)
        - qAC * abs(qAC)
        + qBD * abs(qBD)
        - qCD * abs(qCD)
    )

    # 7) Loop 2: qCD|qCD| - 0.5 qCE|qCE| + 1.5 qDE|qDE|
    Fx[6] = (
        qCD * abs(qCD)
        - 0.5 * qCE * abs(qCE)
        + 1.5 * qDE * abs(qDE)
    )

    # 8) Energy: (p0-p1)/K + q1A|q1A| + qAC|qAC| + 0.5 qCE|qCE| + qE0|qE0|
    Fx[7] = (
        const_energy
        + q1A * abs(q1A)
        + qAC * abs(qAC)
        + 0.5 * qCE * abs(qCE)
        + qE0 * abs(qE0)
    )

    return Fx


def DF(x):
    """
    Jacobi fylkið DF(x) for the above F(x)
    Uses d/dx (x|x|) = 2|x|
    """
    q1A, qAB, qAC, qBD, qCD, qCE, qDE, qE0 = x

    J = np.zeros((8, 8))

    # Row 1: F1 = q1A - qAB - qAC
    J[0, 0] =  1.0   # d/dq1A
    J[0, 1] = -1.0   # d/dqAB
    J[0, 2] = -1.0   # d/dqAC

    # Row 2: F2 = qAB - qBD + QB
    J[1, 1] =  1.0   # d/dqAB
    J[1, 3] = -1.0   # d/dqBD

    # Row 3: F3 = qAC - qCD - qCE
    J[2, 2] =  1.0   # d/dqAC
    J[2, 4] = -1.0   # d/dqCD
    J[2, 5] = -1.0   # d/dqCE

    # Row 4: F4 = qBD + qCD - qDE
    J[3, 3] =  1.0   # d/dqBD
    J[3, 4] =  1.0   # d/dqCD
    J[3, 6] = -1.0   # d/dqDE

    # Row 5: F5 = qCE + qDE - qE0
    J[4, 5] =  1.0   # d/dqCE
    J[4, 6] =  1.0   # d/dqDE
    J[4, 7] = -1.0   # d/dqE0

    # Row 6: F6 = qAB|qAB| - qAC|qAC| + qBD|qBD| - qCD|qCD|
    J[5, 1] =  2.0 * abs(qAB)   # d/dqAB
    J[5, 2] = -2.0 * abs(qAC)   # d/dqAC
    J[5, 3] =  2.0 * abs(qBD)   # d/dqBD
    J[5, 4] = -2.0 * abs(qCD)   # d/dqCD

    # Row 7: F7 = qCD|qCD| - 0.5 qCE|qCE| + 1.5 qDE|qDE|
    J[6, 4] =  2.0 * abs(qCD)        # d/dqCD
    J[6, 5] = -1.0 * abs(qCE)        # 2 * (-0.5)
    J[6, 6] =  3.0 * abs(qDE)        # 2 * (1.5)

    # Row 8: F8 = const + q1A|q1A| + qAC|qAC| + 0.5 qCE|qCE| + qE0|qE0|
    J[7, 0] = 2.0 * abs(q1A)     # d/dq1A
    J[7, 2] = 2.0 * abs(qAC)     # d/dqAC
    J[7, 5] = 1.0 * abs(qCE)     # 2 * 0.5
    J[7, 7] = 2.0 * abs(qE0)     # d/dqE0

    return J

def newtonmult(x0, tol):
    x = x0.copy()
    oldx = x + 2*tol
    while LA.norm(x - oldx, np.inf) > tol:
        oldx = x.copy()
        s = -LA.solve(DF(x), F(x))
        x = x + s
    return x

# Example usage:
x0 = np.array([1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0])  # or a better guess
tol = 1e-8
sol = newtonmult(x0, tol)
print("solution:", sol)
