import numpy as np
import scipy.sparse as sp


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


