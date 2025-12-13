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


def makePartOfA(jStart, jEnd, iFormula, iPlus, values, jLoc):
    coordVals = set()
    for s, j in enumerate(range(jStart, jEnd+1)):
        i = iFormula(j)
        temp_coords = []
        for k, x in enumerate(values):
            temp_coords.append((x, jLoc, i+iPlus[k]-1))
        coordVals.add(frozenset(temp_coords))
        jLoc += 1
    
    return coordVals, jLoc

def vinstriEfri(n, m, H, K, P, delta, Lx, Ly, L):
    hx = Lx / (m-1)
    
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

    values = [-3, 4, -1]

    return jStart, jEnd, iFormula, iPlus, values

def haegri(n, m, H, K, P, delta, Lx, Ly, L):
    hx = Lx / (m-1)

    jStart = 1
    jEnd = n

    iFormula = lambda j: j*m

    iPlus = [0, -1, -2]

    values = [-3+(2*H*hx)/K, 4, -1]

    return jStart, jEnd, iFormula, iPlus, values

def nidri(n, m, H, K, P, delta, Lx, Ly, L):
    hy = Ly / (n-1)

    jStart = 2
    jEnd = m-1

    iFormula = lambda j: j

    iPlus = [0, m, 2*m]

    values = [-3+(2*H*hy)/K, 4, -1]

    return jStart, jEnd, iFormula, iPlus, values

def uppi(n, m, H, K, P, delta, Lx, Ly, L):
    hy = Ly / (n-1)

    jStart = n*m-m+2
    jEnd = n*m-1

    iFormula = lambda j: j

    iPlus = [0, -m, -2*m]

    values = [-3+(2*H*hy)/K, 4, -1]

    return jStart, jEnd, iFormula, iPlus, values

def innriRod(n, m, H, K, P, delta, Lx, Ly, L, r):
    hx = Lx / (m-1)
    hy = Ly / (n-1)

    jStart = r*m+2
    jEnd = r*m+m-1

    iFormula = lambda j: j

    iPlus = [-m, -1, 0, 1, m]

    values = [hx**2, hy**2, -2*(hx**2+hy**2+(H*(hx**2)*(hy**2))/(K*delta)), hy**2, hx**2]

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

def doEverything(n, m, H=0.005, K=1.68, P=5, delta=0.1, Lx=2, Ly=2, L=2, U=20):
    hx = Lx/(m-1)

    breytur = [n, m, H, K, P, delta, Lx, Ly, L]

    jLoc_use = 0
    innriPunktar = set()
    for k in range(1, n-1):   
        inner_row, jLoc = makePartOfA(*innriRod(*breytur, k), jLoc_use)
        jLoc_use = jLoc
        for x in inner_row:
            innriPunktar.add(x)
    a1 = vinstriEfri(*breytur)
    a2 = vinstriNedri(*breytur)
    a3 = nidri(*breytur)
    a4 = uppi(*breytur)
    a5 = haegri(*breytur)
    
    vinstriEfri, jLoc0 = makePartOfA(*a1, jLoc)
    vinstriNedri, jLoc1 = makePartOfA(*a2, jLoc0)
    nidri, jLoc0 = makePartOfA(*a3, jLoc1)
    uppi, jLoc1 = makePartOfA(*a4, jLoc0)
    haegri, jLoc0 = makePartOfA(*a5, jLoc1)

    megalist = [
        *[x for y in vinstriEfri for x in y],
        *[x for y in vinstriNedri for x in y],
        *[x for y in nidri for x in y],
        *[x for y in uppi for x in y],
        *[x for y in haegri for x in y],
        *[x for y in innriPunktar for x in y]
    ]

    _, vinstriNedriRows, _ = zip(*[x for y in vinstriNedri for x in y])
    length = len(list(set(vinstriNedriRows)))

    vinstriNedriRows = np.array(list(set(vinstriNedriRows)))
    bValues = np.array([-2*P*hx/(L*delta*K) for _ in range(length)])
    columns = np.array([0 for x in range(length)])

    b = sp.coo_matrix((bValues, (vinstriNedriRows, columns)), shape=(n*m, 1)).tocsr()

    values, rows, cols = map(np.array, zip(*megalist))
    A = sp.coo_matrix((values, (rows, cols)), shape=(n*m, n*m)).tocsr()

    sol = sp.linalg.spsolve(A, b)

    u = np.asarray(sol).reshape((n, m))

    T = u + U                         

    plt.imshow(T, origin="lower", extent=[0, Lx, 0, Ly], aspect="auto")
    plt.colorbar(label="Temperature (°C)")
    plt.xlabel("x (cm)")
    plt.ylabel("y (cm)")
    plt.show()