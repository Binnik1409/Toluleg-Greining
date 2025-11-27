import numpy as np
import math as m
from functions import q_E0
from functions import poisuilles

# Gera fall af q_E0 sem skilar P1
def tralla(q_E0,p_0):

    G = (m.pi * ((5e-2)**4)) / (8 * (1e-3) * 100)

    for q in q_E0:
        
        P_E = (q/G)+p_0
        P_D = 




# Skilgreina fasta
w = 2 * np.pi / 24
A = 1.32094476
B = 4.01567095
C = 9.45

# Búa til tíma vigur fyrir 100 tímaeiningar á einum sólahring
time = [24/100 * i for i in range(1, 101)]

# Finna q_E0 gildin með jöfnu 18.
list_of_q_E0 = []
for t in time:
    q = q_E0(A, B, C, w, t)
    list_of_q_E0.append(q)

<<<<<<< HEAD
print(list_of_p1  )
=======



def p1_poisuilles(p1):

    G = (m.pi * ((5e-2)**4)) / (8 * (1e-3) * 100)

    x = np.array([
        2982653.95529531,
        2711991.61935227,
        2035970.24653365,
        2156123.62538856,
        1502551.70272537
    ])

    p0 = 0
    q = poisuilles(x, G, p1, p0)

    # Return q_E0 (last element)
    return q[-1]
>>>>>>> f4170b9 (fdsjfkhsgrkd)
