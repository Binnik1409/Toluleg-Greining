import numpy as np
from functions import newton

f = lambda s: 2*s**4 + 23*s**3 + 45*s**2 + 60*s + 50
Df = lambda s: 8*s**3 + 69*s**2 + 90*s + 60

p = -5j
tol = 10**(-10)

x1 = newton(p, tol, f, Df, errors=True)
print(x1[0])

x2 = np.conj(x1[0])
print(x2)

samleitni = []
for i in range(len(x1[1])-1):
    samleitni.append(x1[1][i+1]/(x1[1][i]**2))

print("|         Villur         |         Samleitni         |")
for i in range(len(x1[1])):
    try:
        print("|  ", x1[1][i], "  |  ", samleitni[i], "  |")
    except:
        print("|  ", x1[1][i], "  |  ", "  |")

