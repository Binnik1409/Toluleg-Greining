import numpy as np
import scipy.sparse as sp
import math
import functions as f
import matplotlib.pyplot as plt

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


def makePartOfA(jStart, jEnd, iFormula, iPlus, values):
    coordVals = set()
    for s, j in enumerate(range(jStart, jEnd+1)):
        i = iFormula(j)
        for k, x in enumerate(values):
            coordVals.add((i+iPlus[k], x))
    return coordVals

# def makeA(n, m, H, K, P, delta, Lx, Ly, L):

def vinstriEfri(n, m, H, K, P, delta, Lx, Ly, L):
    hx = Lx / m
    
    jStart = math.floor((L/Ly)*(n-1))+1
    jEnd = n-1

    iFormula = lambda j: j*m+1
    
    iPlus = [0, 1, 2]

    values = [(2*H*hx/K)-3, 4, -1]

    return jStart, jEnd, iFormula, iPlus, values

def vinstriNedri(n, m, H, K, P, delta, Lx, Ly, L):
    jStart = 0
    jEnd = math.floor((L/Ly)*(n-1))

    iFormula = lambda j: j*m+1

    iPlus = [0, 1, 2]

    values = [3*L*delta*K, -4*L*delta*K, L*delta*K]

    return jStart, jEnd, iFormula, iPlus, values

def hageri(n, m, H, K, P, delta, Lx, Ly, L):
    hx = Lx / m

    jStart = 1
    jEnd = n

    iFormula = lambda j: j*m

    iPlus = [1, -1, -2]

    values = [-3+(2*H*hx)/K, 4, -1]

    return jStart, jEnd, iFormula, iPlus, values

def nidri(n, m, H, K, P, delta, Lx, Ly, L):
    hy = Ly / n

    jStart = 2
    jEnd = m-1

    iFormula = lambda j: j

    iPlus = [0, m, 2*m]

    values = [-3+(2*H*hy)/K, 4, -1]

    return jStart, jEnd, iFormula, iPlus, values

def uppi(n, m, H, K, P, delta, Lx, Ly, L):
    hy = Ly / n

    jStart = n*m-m+1
    jEnd = n*m-1

    iFormula = lambda j: j

    iPlus = [0, -m, -2*m]

    values = [-3+(2*H*hy)/K, 4, -1]

    return jStart, jEnd, iFormula, iPlus, values

def innriRod(n, m, H, K, P, delta, Lx, Ly, L, r):
    hx = Lx / m
    hy = Ly / n

    jStart = r*m+2
    jEnd = r*m+m-1

    iFormula = lambda j: j

    iPlus = [-m, -1, 0, 1, m]

    values = [hx**2, hy**2, ((2*H))]

    return jStart, jEnd, iFormula, iPlus, values

def index_to_xy_zero(idx, n, m):
    """Convert dot index → (x, y) in Python 0-based indexing."""
    idx -= 1
    y = idx // m
    x = idx % m
    return x, y

def build_system(breytur: list): 
    '''Breytur = [n, m, H, K, P, delta, Lx, Ly, L]'''

    vinstriEfriA = f.makePartOfA(*f.vinstriEfri(*breytur))
    vinstriNedriA = f.makePartOfA(*f.vinstriNedri(*breytur))
    nidriA = f.makePartOfA(*f.nidri(*breytur))
    uppiA = f.makePartOfA(*f.uppi(*breytur))
    haegriA = f.makePartOfA(*f.hageri(*breytur))
    innriRod1 = f.makePartOfA(*f.innriRod(*breytur,1))
    innriRod2 = f.makePartOfA(*f.innriRod(*breytur,2))
    innriRod3 = f.makePartOfA(*f.innriRod(*breytur,3))  

    # Build matrix a from parts hear
    all_parts = [
        vinstriEfriA,
        vinstriNedriA,
        nidriA,
        uppiA,
        haegriA,
        innriRod1,
        innriRod2,
        innriRod3
    ]

    vals = [] 
    x_idx = []
    y_idx = []
    for part in all_parts:
        for dot_index, val in part:
            x, y = index_to_xy_zero(dot_index, breytur[0], breytur[1])
            vals.append(val)
            x_idx.append(x)
            y_idx.append(y)

    A = sp.csr_matrix((vals, (x_idx, y_idx)), shape=(breytur[0]+1, breytur[1]+1))
    plt.imshow(A.toarray())
    return A