import numpy as np
import scipy.sparse as sp


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

     
