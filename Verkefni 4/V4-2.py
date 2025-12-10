import numpy as np
import scipy.sparse as sp
import functions as f


### Fastar ###
Lx = Ly = 2
L = 5
delta = 0.1
P = 5
K = 1.68
H = 0.005
# Upphafshitastig er 20 gráður Celsíus
# Jöfnurnar gera ráð fyrir hitastigi 0 gráður Celsíus
# Því þarf að bæta 20 gráðum við niðurstöðuna til að fá rétta lausn
Upphafshitastig = 20

m = n = 10


## Fyrsta og seinasta lína í A
a = 1
b = 2
c = 3
alpha = 0.5

i, j, gildi = f.build_part_of_A(n, a, b, c, alpha)



    


A = sp.coo_matrix((gildi, (i, j))).tocsc()

