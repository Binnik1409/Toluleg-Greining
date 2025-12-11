import numpy as np
import scipy.sparse as sp
import math


def build_part_of_A(n, a, b, c, alpha):        

    i = [] 
    j = []
    gildi = []

    for k in range(n):
        
        if k==0:
            i.append(k)
            i.append(k)
            i.append(k)
            j.append(k)
            j.append(k+1)
            j.append(k+2)
            gildi.append(a)
            gildi.append(b)
            gildi.append(c)
        if k==n:
            i.append(k)
            i.append(k)
            i.append(k)
            j.append(k)
            j.append(k+1)
            j.append(k+2)
            gildi.append(c)
            gildi.append(b)
            gildi.append(a)
        else:
            i.append(k)
            i.append(k+1)
            i.append(k+2)
            j.append(k)
            j.append(k+1)
            j.append(k+2)
            gildi.append(1)
            gildi.append(alpha)
            gildi.append(1)
        
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
    
