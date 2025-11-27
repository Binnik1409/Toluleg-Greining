import numpy as np
import math as m
from functions import q_E0
from functions import poisuilles

# Gera posisuilles fallið að falli af p1
def p1_poisuilles(p1):

    G = (m.pi*((5*10**(-2))**4))/(8*(1*10**(-3))*100)
    x = np.array([
    2982653.95529531,
    2711991.61935227,
    2035970.24653365,
    2156123.62538856,
    1502551.70272537
    ])  
    p0 = 0
    q = poisuilles(x,G,p1,p0)
    return q[7]

def bisection(f,a,b,tol,r_value):
    '''gert ráð fyrir að búið se að skilgreina f(x) fyrir utan t.d.
    def f(x):
        return(x**2-2)
    '''
    fa = f(a)
    fb = f(b)
    while (b-a)/2>tol:
        c=(a+b)/2
        fc=f(c)
        if fc==r_value:break
        if abs(fc-r_value) < abs(fb-r_value):
            b=c
        else:
            a=c
            fa=fc
    return((a+b)/2)

# Skilgreina fasta
w = 2*np.pi/24
A = 1.32094476 
B = 4.01567095 
C = 9.45

# Búa til tíma vigur fyrir 100 tímaeiningar á einum sólahring
time = [24/100*i for i in range(1,101)]

list_of_p1 = []
for t in time:
    q = q_E0(A,B,C,w,t)
    p1 = bisection(p1_poisuilles,0,4.2*10**(6),1e-8,q)
    list_of_p1.append(p1)    

print(list_of_p1  )
