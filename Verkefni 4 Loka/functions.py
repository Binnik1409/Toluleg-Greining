import numpy as np
import scipy.sparse as sp
import math
import functions as f
import matplotlib.pyplot as plt


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


def build_system(breytur: list): 
    '''Breytur = [n, m, H, K, P, delta, Lx, Ly, L]'''

    N = breytur[0] * breytur[1]

    vinstriEfriA = f.makePartOfA(*f.vinstriEfri(*breytur))
    vinstriNedriA = f.makePartOfA(*f.vinstriNedri(*breytur))
    nidriA = f.makePartOfA(*f.nidri(*breytur))
    uppiA = f.makePartOfA(*f.uppi(*breytur))
    haegriA = f.makePartOfA(*f.haegri(*breytur))
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

    rows = []
    cols = []
    vals = []

    for part in all_parts:
        for idx, val in part:
            row = idx - 1
            rows.append(row)
            cols.append(row)
            vals.append(val)

        A = sp.csr_matrix((vals, (rows, cols)), shape=(N, N))

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

def vinstriKalt(n, m, H, K, P, delta, Lx, Ly, L, jStart, jEnd):
    hx = Lx / (m-1)
    
    # jStart = math.floor((L/Ly)*(n-1))+1
    # jEnd = n-1

    iFormula = lambda j: j*m+1
    
    iPlus = [0, 1, 2]

    values = [(2*H*hx/K)-3, 4, -1]

    return jStart, jEnd, iFormula, iPlus, values

def vinstriHeitt(n, m, H, K, P, delta, Lx, Ly, L, jStart, jEnd):
    # jStart = 0
    # jEnd = math.floor((L/Ly)*(n-1))

    iFormula = lambda j: j*m+1

    iPlus = [0, 1, 2]

    values = [-3, 4, -1]

    return jStart, jEnd, iFormula, iPlus, values


def best_cpu_placement(Lx=10, Ly=10, delta=0.1, P=5, K=1.68, H=0.005, U=20, n=200, m=200, POWER_START=0, POWER_END=9,L=9):


    hot_start = math.ceil(n*POWER_START/Ly)
    hot_end = math.floor(n*POWER_END/Ly)
    hx = Lx/(m-1)

    breytur = [n, m, H, K, P, delta, Lx, Ly, L]

    jLoc_use = 0
    innriPunktar = set()
    for k in range(1, n-1):   
        inner_row, jLoc = f.makePartOfA(*f.innriRod(*breytur, k), jLoc_use)
        jLoc_use = jLoc
        for x in inner_row:
            innriPunktar.add(x)


    vinstriKalt1, jLoc0 = f.makePartOfA(*vinstriKalt(*breytur, 0, hot_start-1), jLoc)
    vinstriKalt2, jLoc1 = f.makePartOfA(*vinstriKalt(*breytur, hot_end+1, n-1), jLoc0)
    vinstriEfri, jLoc0 = vinstriKalt1.union(vinstriKalt2), jLoc1
    vinstriNedri, jLoc1 = f.makePartOfA(*vinstriHeitt(*breytur, hot_start, hot_end), jLoc0)
    nidri, jLoc0 = f.makePartOfA(*f.nidri(*breytur), jLoc1)
    uppi, jLoc1 = f.makePartOfA(*f.uppi(*breytur), jLoc0)
    haegri, jLoc0 = f.makePartOfA(*f.haegri(*breytur), jLoc1)

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
    bValues = (-2*P*hx/(L*delta*K))*np.ones(length)
    columns = np.zeros(length)

    b = sp.coo_matrix((bValues, (vinstriNedriRows, columns)), shape=(n*m, 1)).tocsr()

    values, rows, cols = map(np.array, zip(*megalist))
    A = sp.coo_matrix((values, (rows, cols)), shape=(n*m, n*m)).tocsr()

    sol = sp.linalg.spsolve(A, b)

    u = np.asarray(sol).reshape((n, m))

    T = u + U
    
    return T