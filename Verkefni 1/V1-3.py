import numpy as np
import matplotlib.pyplot as plt
from functions import goldensearch, cfunc

a = 0
b = 30

tol = 10**(-10)

c_vals = np.linspace(a, b, 1000)
c = []
for i in c_vals:
    c.append(cfunc(i, tol))

c0 = goldensearch(a, b, tol, cfunc)

print(c0)

plt.plot(c_vals, c)
plt.axvline(c0, linestyle = "--")
plt.xlabel("c1")
plt.ylabel("Raunhluti tvinntölurótar")
plt.title("Gullsniðs leitaraðferð fyrir minnstu tvinntölurót")
plt.legend(["Raunhluti tvinntölurótar sem fall af c1", f"Gildi c1 fyrir minnstu tvinntölurót: ~{round(c0, 3)}"])
plt.grid()
plt.show()
