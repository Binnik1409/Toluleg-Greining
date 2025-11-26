import math
import numpy as np
from numpy import linalg as la


def bisection(f,a,b,tol):
    '''gert ráð fyrir að búið se að skilgreina f(x) fyrir utan t.d.
    def f(x):
        return(x**2-2)
    '''
    if f(a)*f(b) >= 0:
        print("Bisection method fails.")
        return None
    else:
        fa=f(a)
        while (b-a)/2>tol:
            c=(a+b)/2
            fc=f(c)
            if fc==0:break
            if fc*fa<0:
                b=c
            else:
                a=c
                fa=fc
    return((a+b)/2)

def goldensearch(a,b,tol,f):
    phi=(math.sqrt(5)-1)/2
    x1=a+(1-phi)*(b-a)
    x2=a+phi*(b-a)
    f1=f(x1)
    f2=f(x2)
    while (b-a)/2>tol:
        if f1<f2:
            b=x2
            x2=x1
            x1=a+(1-phi)*(b-a)
            f2=f1
            f1=f(x1)
        else:
            a=x1
            x1=x2
            x2=a+phi*(b-a)
            f1=f2
            f2=f(x2)
    return((a+b)/2)

def newton(x0,tol, f, Df, errors = False):
    oldx=x0+2*tol
    x=x0
    if errors:
        errors = []
        while abs(oldx-x)>tol:
            oldx=x
            x=x-f(x)/Df(x)
            errors.append(abs(oldx-x))
        return x, errors
    else:
        while abs(oldx-x)>tol:
            oldx=x
            x=x-f(x)/Df(x)
        return x
    
def newtonmult(x0,tol,F,DF):
    '''
    x0 er vigur i R^n skilgreindur t.d. sem
    x0=np.array([1,2,3])
    gert ráð fyrir að F(x) og Jacobi fylki DF(x) séu skilgreind annars staðar
    '''
    x=x0
    oldx=x+2*tol
    while la.norm(x-oldx,np.inf)>tol:
        oldx=x
        s=-la.solve(DF(x),F(x))
        x=x+s
    return(x)

def qE0(t, A, B, C, w=2*np.pi/24):
    return(A*np.cos(float(w)*float(t))+B*np.sin(float(w)*float(t))+C)

def poisuilles(x,G,p1,p0):

    poisuilles_gildi = [
    (G,   p1,  x[0]),       # q_1A 
    (G,   x[0], x[1]),      # q_AB 
    (G,   x[0], x[2]),      # q_AC 
    (G,   x[1], x[3]),      # q_BD 
    (G,   x[2], x[3]),      # q_CD 
    (G,   x[2], x[4]),      # q_CE 
    ((2/3)*G, x[3], x[4]),  # q_DE 
    (G,   x[4], p0)         # q_E0 
    ]
    q = [g * (i - j) for g, i, j in poisuilles_gildi] #[q_1A, q_AB, q_AC, q_BD, q_CD, q_CE, q_DE, q_E0]
   
    return q


def F(q,QB,p0,p1,K):

    results = np.array([
        q[0]-q[1]-q[2],
        QB+q[1]-q[3],
        q[2]-q[4]-q[5],
        q[3]+q[4]-q[6],
        q[5]+q[6]-q[7],
        q[1]*abs(q[1])-q[2]*abs(q[2])+q[3]*abs(q[3])-q[4]*abs(q[4]),
        q[4]*abs(q[4])-1/2*q[5]*abs(q[5])+3/2*q[6]*abs(q[6]),
        (p0-p1)/K+q[0]*abs(q[0])+q[2]*abs(q[2])+1/2*q[5]*abs(q[5])+q[7]*abs(q[7])
        ])
    
    return results
