import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as spla
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

import numpy as np
from scipy.sparse import lil_matrix, csr_matrix
from scipy.sparse.linalg import spsolve

import numpy as np
from scipy.sparse import lil_matrix, csr_matrix
from scipy.sparse.linalg import spsolve

def heatsink_fd(Lx, Ly, delta, H, K, P, nx, ny, L_in, T_amb=20):
    """
    Builds sparse matrix A and vector B for the steady-state temperature distribution
    of a rectangular fin (heatsink blade) using finite differences, including ambient temperature.

    Parameters:
    Lx, Ly : float - size of the blade (m)
    delta : float - thickness (m)
    H : float - convective heat transfer coefficient (W/m^2K)
    K : float - thermal conductivity (W/mK)
    P : float - total power input (W)
    nx, ny : int - number of grid points in x and y
    L_in : float - length of power input at left edge (m)
    T_amb : float - ambient temperature (°C)

    Returns:
    A : csr_matrix - sparse system matrix
    B : ndarray - RHS vector including ambient temperature
    """
    dx = Lx / (nx - 1)
    dy = Ly / (ny - 1)
    N = nx * ny

    A = lil_matrix((N, N))
    B = np.zeros(N)

    def idx(i, j):
        return j * nx + i

    for j in range(ny):
        for i in range(nx):
            k = idx(i, j)

            # Interior points
            if 0 < i < nx-1 and 0 < j < ny-1:
                A[k, idx(i,j)] = -2/dx**2 - 2/dy**2 + 2*H/(K*delta)
                A[k, idx(i+1,j)] = 1/dx**2
                A[k, idx(i-1,j)] = 1/dx**2
                A[k, idx(i,j+1)] = 1/dy**2
                A[k, idx(i,j-1)] = 1/dy**2
                B[k] = 2*H/(K*delta) * T_amb  # ambient contribution

            else:
                # Left edge
                if i == 0:
                    if j*dy <= L_in:  # Power input region
                        # u1 - u0 / dx = -P/(L δ K)
                        A[k, idx(i,j)] = 1
                        A[k, idx(i+1,j)] = -1
                        B[k] = dx * P / (L_in * delta * K) + T_amb  # include ambient
                    else:  # Convection
                        A[k, idx(i,j)] = 1/dx + H/K
                        A[k, idx(i+1,j)] = -1/dx
                        B[k] = H/K * T_amb  # convection to ambient
                # Right edge (convection)
                elif i == nx-1:
                    A[k, idx(i,j)] = 1/dx + H/K
                    A[k, idx(i-1,j)] = -1/dx
                    B[k] = H/K * T_amb
                # Bottom edge (convection)
                elif j == 0:
                    A[k, idx(i,j)] = 1/dy + H/K
                    A[k, idx(i,j+1)] = -1/dy
                    B[k] = H/K * T_amb
                # Top edge (convection)
                elif j == ny-1:
                    A[k, idx(i,j)] = 1/dy + H/K
                    A[k, idx(i,j-1)] = -1/dy
                    B[k] = H/K * T_amb

    A_csr = csr_matrix(A)
    return A_csr, B

# ---------------- Example usage ----------------
Lx = 0.1      # meters
Ly = 0.05
delta = 0.002
H = 10        # W/m^2K
K = 200       # W/mK
P = 50        # W
nx, ny = 20, 10
L_in = 0.02

A, B = heatsink_fd(Lx, Ly, delta, H, K, P, nx, ny, L_in)

# Solve the system
u = spsolve(A, B)

# Reshape solution into 2D grid for plotting
U = u.reshape((ny, nx))
print("Temperature at each grid point:")
print(U)



def idx(i, j, n):
    """Convert (i,j) grid index into vector index."""
    return j + i*n

def build_system(m, n, Lx, Ly, K, H, delta, P, L):

    hx = Lx/(m)
    hy = Ly/(n)
    alpha = 2*H/(K*delta)

    N = m*n
    A = sp.lil_matrix((N, N))
    b = np.zeros(N)

    for i in range(m):
        for j in range(n):
            k = idx(i, j, n)


            # interior point
            if 0 < i < m-1 and 0 < j < n-1:
                A[k, idx(i, j, n)] = -2/hx**2 - 2/hy**2 - alpha
                A[k, idx(i-1, j, n)] = 1/hx**2
                A[k, idx(i+1, j, n)] = 1/hx**2
                A[k, idx(i, j-1, n)] = 1/hy**2
                A[k, idx(i, j+1, n)] = 1/hy**2
                continue

            # boundary conditions:
            # Left boundary (x = 0)
            if i == 0:

                A[k, k] = -1/hx - H/K
                A[k, idx(1, j, n)] = 1/hx

                if j*hy <= L:
                    # LOWER HALF: heat input BC
                    b[k] = -P / (L * delta * K)

                else:
                    # UPPER HALF: convection BC
                    b[k] = 0

                continue


            # Right boundary x=Lx
            if i == m-1:
                A[k, k] = 1/hx + H/K
                A[k, idx(i-1, j, n)] = -1/hx
                continue

            # Bottom boundary y=0
            if j == 0:
                A[k, k] = -1/hy - H/K
                A[k, idx(i, j+1, n)] = 1/hy
                continue

            # Top boundary y=Ly
            if j == n-1:
                A[k, k] = 1/hy + H/K
                A[k, idx(i, j-1, n)] = -1/hy
                continue

    return A.tocsr(), b

def solve_with_offset(m, n, offset, L, Lx, Ly, K, H, delta, P):
    """
    Solve heat distribution when heat input is applied on the left boundary
    only on the interval y ∈ [offset, offset + L].

    Returns:
        max temperature (in °C above ambient),
        full grid solution U (m×n array)
    """

    hx = Lx / (m - 1)
    hy = Ly / (n - 1)
    alpha = 2 * H / (K * delta)

    N = m * n
    A = sp.lil_matrix((N, N))
    b = np.zeros(N)

    def is_heat_segment(y):
        """Return True if y coordinate lies inside the heating interval."""
        return offset <= y <= offset + L

    for i in range(m):
        for j in range(n):
            k = idx(i, j, n)
            x = i * hx
            y = j * hy

            # -----------------------------
            # Interior points
            # -----------------------------
            if 0 < i < m - 1 and 0 < j < n - 1:
                A[k, k] = -2/hx**2 - 2/hy**2 - alpha
                A[k, idx(i-1, j, n)] = 1/hx**2
                A[k, idx(i+1, j, n)] = 1/hx**2
                A[k, idx(i, j-1, n)] = 1/hy**2
                A[k, idx(i, j+1, n)] = 1/hy**2
                continue

            # -----------------------------
            # Left boundary x = 0
            # -----------------------------
            if i == 0:

                # Apply heating only on offset ≤ y ≤ offset + L
                if is_heat_segment(y):
                    A[k, k] = -1/hx
                    A[k, idx(1, j, n)] = 1/hx
                    b[k] = -P / (L * delta * K)
                else:
                    A[k, k] = -1/hx - H/K
                    A[k, idx(1, j, n)] = 1/hx
                    b[k] = 0
                continue

            # -----------------------------
            # Right boundary x = Lx
            # -----------------------------
            if i == m - 1:
                A[k, k] = 1/hx + H/K
                A[k, idx(i-1, j, n)] = -1/hx
                continue

            # -----------------------------
            # Bottom boundary y = 0
            # -----------------------------
            if j == 0:
                A[k, k] = -1/hy - H/K
                A[k, idx(i, j+1, n)] = 1/hy
                continue

            # -----------------------------
            # Top boundary y = Ly
            # -----------------------------
            if j == n - 1:
                A[k, k] = 1/hy + H/K
                A[k, idx(i, j-1, n)] = -1/hy
                continue

    # Convert to CSR and solve
    A = A.tocsr()
    v = spla.spsolve(A, b)
    U = v.reshape((m, n))

    return U.max(), U


def maxT_for_power(P,m,n,Lx,Ly,K,H,delta,L):
    A, b = build_system(m, n, Lx, Ly, K, H, delta, P, L)
    v = spla.spsolve(A, b)
    return v.max() + 20   # add ambient