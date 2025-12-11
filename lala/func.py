import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as spla
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D



def idx(i, j, n):
    """Convert (i,j) grid index into vector index."""
    return j + i*n

def build_system(m, n, Lx, Ly, K, H, delta, P, L):
    hx = Lx/(m-1)
    hy = Ly/(n-1)

    alpha = 2*H/(K*delta)

    N = m*n
    A = sp.lil_matrix((N, N))
    b = np.zeros(N)

    for i in range(m):
        for j in range(n):
            k = idx(i, j, n)

            x = i*hx
            y = j*hy

            # interior point
            if 0 < i < m-1 and 0 < j < n-1:
                A[k, idx(i, j, n)] = -2/hx**2 - 2/hy**2 - alpha
                A[k, idx(i-1, j, n)] = 1/hx**2
                A[k, idx(i+1, j, n)] = 1/hx**2
                A[k, idx(i, j-1, n)] = 1/hy**2
                A[k, idx(i, j+1, n)] = 1/hy**2
                continue

            # boundary conditions:
            # Left boundary x=0
            if i == 0:
                A[k, k] = -1/hx - H/K

                # Is this point in the heat input segment?
                if y <= L:
                    b[k] = -P/(L*delta*K)
                else:
                    b[k] = 0
                A[k, idx(i+1, j, n)] = 1/hx
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
                A[k, k] = -1/hx - H/K
                A[k, idx(1, j, n)] = 1/hx

                # Apply heating only on offset ≤ y ≤ offset + L
                if is_heat_segment(y):
                    b[k] = -P / (L * delta * K)
                else:
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