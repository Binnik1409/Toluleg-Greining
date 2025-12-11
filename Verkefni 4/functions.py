import numpy as np
import scipy.sparse as sp
import math
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

     

def Avinstri(n, m, H, K, delta, hx, Ly, L):
    length = n
    rows = np.zeros(length)
    top_hot = math.floor((L/Ly)*n)

    for k,i in enumerate([j*m+1 for j in range(2)]):
        rows[k][i] = 3*L*delta*K
        rows[k][i+1] = -4*L*delta*K
        rows[k][i+2] = L*delta*K
    for k,i in enumerate([j*m+1 for j in range(2, top_hot+1)]):
        k=k+2
        rows[k][i] = 3*L*delta*K
        rows[k][i-1] = -4*L*delta*K
        rows[k][i-2] = L*delta*K
    for k, i in enumerate([j*m+1 for j in range(top_hot+1, n)]):
        k=k+top_hot+1
        rows[k][i] = -(2*H*hx/K)-3
        rows[k][i] = 4
        rows[k][i] = -1
    return rows

def bvinstri(n, P, hx, Ly, L):
    b = np.zeros(n)
    top_hot = math.floor((L/Ly)*n)

    for i in range(2):
        b[i] = 2*P*hx
    for i in range(2, n-top_hot+1):
        b[i] = -2*P*hx

def Anidri(n, m, H, K, hy):
    length = len(range(2, m-1+1))
    rows = np.zeros((length, n*m))

    for k, i in enumerate([j for j in range(2, m-1+1)]):
        rows[k][i] = ((2*H*hy/K)-3)
        rows[k][i+m] = 4
        rows[k][i+m] = -1
    return rows
        
def bnidri(m):
    return np.zeros(len(range(2, m-1+1)))

def Ahaegri(n, m, H, K, hy):
    length = Ly - L // Ly
    rows = np.zeros((length, n*m))

    for k, i in enumerate([j*m for j in range(1, n-2+1)]):
        rows[k][i] = ((-2*H*hy/K)-3)
        rows[k][i+1] = 4
        rows[k][i+2] = -1
    for k,i in enumerate([j*m for j in range(n-1, n+1)]):
        rows[k][i] = ((2*H*hy/K)-3)
        rows[k][i-1] = 4
        rows[k][i-2] = -1
    return rows

def bhaegri(n):
    return np.zeros(n)

def Auppi(n, m, H, K, hy):
    length = [x for x in range(m*n-(m-1), m*n-1+1)]
    rows = np.zeros(length)

    for k,i in enumerate([x for x in range(m*n-(m-1), m*n-3+1)]):
        rows[k][i] = 2*H*hy*+3*K
        rows[k][i+1] = -4
        rows[k][i+2] = 1
    for k,i in enumerate([x for x in range(m*n-3+1, m*n-1+1)]):
        k=k+m*n-3+1
        rows[k][i] = -2*H*hy*+3*K
        rows[k][i-1] = -4
        rows[k][i-2] = 1

def buppi(n, m):
    length = [x for x in range(m*n-(m-1), m*n-1+1)]
    return np.zeros(length)

def Ainnri(n, m, H, K, delta, hx, hy Ly, L):
    


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

def plot_solution(u, n, Lx, Ly):
    """
    Plots the solution vector u as a heatmap.
    
    Parameters:
    u : numpy array
        The solution vector of size n*n.
    n : int
        The number of interior points in each dimension.
    Lx : float
        The length of the domain in the x-direction.
    Ly : float
        The length of the domain in the y-direction.
    """
    # Reshape u into a 2D array for plotting
    U = u.reshape((n, n))
    
    # Create grid for plotting
    x = np.linspace(0, Lx, n)
    y = np.linspace(0, Ly, n)
    X, Y = np.meshgrid(x, y)
    
    # Plotting
    plt.figure(figsize=(8, 6))
    cp = plt.contourf(X, Y, U, levels=50, cmap='viridis')
    plt.colorbar(cp)
    plt.title('Heatmap of the Solution')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.show()
