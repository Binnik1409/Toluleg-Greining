import sys
import os
import numpy as np
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from newton import newton

f = lambda s: 2*s**4 + 23*s**3 + 45*s**2 + 60*s + 50
Df = lambda s: 8*s**3 + 69*s**2 + 90*s + 60

p = 1j
tol = 10**(-3)

x1 = newton(p, tol, f, Df)
print(x1)

x2 = np.conj(x1)
print(x2)
