import functions as f
import numpy as np


def make_matrix(n,m,Lx,Ly,L,P,K,H,initial_temp=0):

    dx = Lx / n
    dy = Ly / m

    matrix = np.zeros((n,m))
    for m,j in enumerate(range(0,Ly,dy)):
        for n,i in enumerate(range(0,Lx,dx)):

            if i <= Lx/2 and j <= L: # vinstra megin, neðri hluti
                ...
            elif i <= Lx/2 and j > L: # vinstra megin, efri hluti
                ...
            elif i > Lx/2 and j >= Ly/2: # hægra megin, efri hluti
                ...
            else: # hægra megin, neðri hluti
                ...

    return matrix