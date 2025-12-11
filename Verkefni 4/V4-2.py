import numpy as np
from scipy.sparse import coo_matrix
from scipy.sparse.linalg import spsolve
import matplotlib.pyplot as plt

# ---------------------------
# Physical parameters (user)
# ---------------------------
Lx = 2.0          # cm
Ly = 2.0          # cm
delta = 0.1       # cm
P = 5.0           # W total power injected
k = 1.68          # W/(cm·°C)
H = 0.005         # W/(cm²·°C)
T_inf = 20.0      # °C

# Length of the heated segment on the left boundary
L_in = 1.0        # cm  (uniform heat flux only in y ∈ [0, L_in])

# ---------------------------
# Discretization
# ---------------------------
m = 41
n = 41
hx = Lx / (m - 1)
hy = Ly / (n - 1)

alpha = k / (hy**2)
beta = k / (hx**2)
center_coef = -2.0 * (alpha + beta)

# --------------------------------------------
# Compute uniform flux only on heated segment
# --------------------------------------------
# Total heated length = L_in
# Total applied power = P
# Thus uniform q'' (W/cm²) is:
q_in = P / (L_in * delta)

# ---------------------------
# Sparse matrix assembly
# ---------------------------
I = []
J = []
V = []

b = np.zeros((m * n, 1))

def idx(i, j):
    return j * m + i

for j in range(n):
    y = j * hy
    for i in range(m):
        kidx = idx(i, j)

        # Corner nodes -> force to T_inf
        if (i == 0 or i == m-1) and (j == 0 or j == n-1):
            I.append(kidx); J.append(kidx); V.append(1.0)
            b[kidx, 0] = T_inf
            continue

        # Interior
        if 0 < i < m-1 and 0 < j < n-1:
            I.append(kidx); J.append(kidx); V.append(center_coef)
            I.append(kidx); J.append(idx(i-1, j)); V.append(beta)
            I.append(kidx); J.append(idx(i+1, j)); V.append(beta)
            I.append(kidx); J.append(idx(i, j-1)); V.append(alpha)
            I.append(kidx); J.append(idx(i, j+1)); V.append(alpha)
            continue

        # ----------------------------------------------------
        # LEFT boundary: piecewise (heated vs non-heated)
        # ----------------------------------------------------
        if i == 0:

            heated = (0.0 <= y <= L_in)

            # Common stencil coefficients
            coef_center = - (beta + 2.0 * alpha) + (2.0 * H) / hx
            coef_right  = beta

            if j > 0:
                I.append(kidx); J.append(idx(i, j-1)); V.append(alpha)
            if j < n - 1:
                I.append(kidx); J.append(idx(i, j+1)); V.append(alpha)

            I.append(kidx); J.append(idx(i+1, j)); V.append(coef_right)
            I.append(kidx); J.append(kidx); V.append(coef_center)

            # RHS
            if heated:
                # q'' enters the domain (Neumann + convection)
                b[kidx, 0] = (2.0 * q_in) / hx + (2.0 * H * T_inf) / hx
            else:
                # Only convection (no input heat)
                b[kidx, 0] = (2.0 * H * T_inf) / hx

            continue

        # RIGHT boundary (convection only)
        if i == m - 1:
            coef_center = - (beta + 2.0 * alpha) + (2.0 * H) / hx
            coef_left = beta
            if j > 0:
                I.append(kidx); J.append(idx(i, j-1)); V.append(alpha)
            if j < n - 1:
                I.append(kidx); J.append(idx(i, j+1)); V.append(alpha)
            I.append(kidx); J.append(idx(i-1, j)); V.append(coef_left)
            I.append(kidx); J.append(kidx); V.append(coef_center)
            b[kidx, 0] = (2.0 * H * T_inf) / hx
            continue

        # BOTTOM boundary
        if j == 0:
            coef_center = - (2.0 * beta + alpha) + (2.0 * H) / hy
            I.append(kidx); J.append(kidx); V.append(coef_center)
            if i > 0:
                I.append(kidx); J.append(idx(i-1, j)); V.append(beta)
            if i < m - 1:
                I.append(kidx); J.append(idx(i+1, j)); V.append(beta)
            I.append(kidx); J.append(idx(i, j+1)); V.append(alpha)
            b[kidx, 0] = (2.0 * H * T_inf) / hy
            continue

        # TOP boundary
        if j == n - 1:
            coef_center = - (2.0 * beta + alpha) + (2.0 * H) / hy
            I.append(kidx); J.append(kidx); V.append(coef_center)
            if i > 0:
                I.append(kidx); J.append(idx(i-1, j)); V.append(beta)
            if i < m - 1:
                I.append(kidx); J.append(idx(i+1, j)); V.append(beta)
            I.append(kidx); J.append(idx(i, j-1)); V.append(alpha)
            b[kidx, 0] = (2.0 * H * T_inf) / hy
            continue

# ---------------------------
# Solve
# ---------------------------
A = coo_matrix((V, (I, J)), shape=(m * n, m * n)).tocsr()
u = spsolve(A, b)
U = u.reshape((n, m))

plt.figure(figsize=(6,5))
plt.imshow(U, extent=(0, Lx, 0, Ly), origin='lower', aspect='equal')
plt.colorbar(label='°C')
plt.xlabel('x (cm)')
plt.ylabel('y (cm)')
plt.title('Temperature (°C)')
plt.show()

print("Heated segment length L_in =", L_in)
print("Uniform q'' =", q_in, "W/cm^2")
print("Temperature range:", np.min(U), np.max(U))
