import sys
sys.path.append('..')
from newton import newton

f = lambda s: 2*s**4 + 23*s**3 + 45*s**2 + 60*s + 50
Df = lambda s: 8*s**3 + 69*s**2 + 90*s + 60

punktar = [-9.45, -1.4]
tol = 10**(-3)

for i in punktar:
    x = newton(i, tol, f, Df)
    print(x)
