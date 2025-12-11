import numpy as np
import scipy.sparse as sp
import functions as f
import matplotlib.pyplot as plt

def build_part_of_A(n, a, b, c, alpha, theta):        

    i = [] 
    j = []
    gildi = []

    for k in range(n):
        
        if k==0:
            i += [k, k, k]
            j += [k, k+1, k+2]
            gildi += [a, b, c]
        if k==n:
            i += [k, k, k]
            j += [k, k-1, k-2]
            gildi += [c, b, a]
        else:
            i += [k, k, k]
            j += [k-1, k, k+1]
            gildi += [theta, alpha, theta]
        
    return i, j, gildi

     
def build_matrix_A_b(n, Lx, Ly, H, K, P, delta, L_input):
    N = n * n
    hx = Lx / (n + 1)
    hy = Ly / (n + 1)
    a = H / K


    # Initialize sparse matrix in LIL format for easy assignment
    A = sp.lil_matrix((N, N))
    b = np.zeros(N)


    for j in range(n):
        y_pos = (j+1) * hy
        for i in range(n):
            idx = j * n + i

            # Main diagonal
            A[idx, idx] = -2/hx**2 -2/hy**2

            # x-direction neighbors
            if i > 0:
                A[idx, idx-1] = 1/hx**2
            else:
                # Left boundary
                if y_pos <= L_input:
                    q = -P / (L_input * delta * K)
                    b[idx] += q * hx
                else:
                    A[idx, idx] -= a / hx
            if i < n-1:
                A[idx, idx+1] = 1/hx**2
            else:
                # Right boundary
                A[idx, idx] -= a / hx


            # y-direction neighbors
            if j > 0:
                A[idx, idx-n] = 1/hy**2
            else:
                # Bottom boundary
                A[idx, idx] -= a / hy
            if j < n-1:
                A[idx, idx+n] = 1/hy**2
            else:
                # Top boundary
                A[idx, idx] -= a / hy

    return A.tocsr(), b