import functions as f
import scipy.sparse as sp
import numpy as np
import matplotlib.pyplot as plt
import time

def solve_once(n):
    Lx = Ly = 2
    delta = 0.1
    P = 5
    K = 1.68
    H = 0.005
    U = 20
    L = 2
    m = n

    hx = Lx/(m-1)

    breytur = [n, m, H, K, P, delta, Lx, Ly, L]

    jLoc_use = 0
    innriPunktar = set()

    for k in range(1, n-1):
        inner_row, jLoc = f.makePartOfA(*f.innriRod(*breytur, k), jLoc_use)
        jLoc_use = jLoc
        for x in inner_row:
            innriPunktar.add(x)

    vinstriEfri, jLoc0 = f.makePartOfA(*f.vinstriEfri(*breytur), jLoc_use)
    vinstriNedri, jLoc1 = f.makePartOfA(*f.vinstriNedri(*breytur), jLoc0)
    nidri, jLoc0 = f.makePartOfA(*f.nidri(*breytur), jLoc1)
    uppi, jLoc1 = f.makePartOfA(*f.uppi(*breytur), jLoc0)
    haegri, jLoc0 = f.makePartOfA(*f.haegri(*breytur), jLoc1)

    megalist = [
        *[x for y in vinstriEfri for x in y],
        *[x for y in vinstriNedri for x in y],
        *[x for y in nidri for x in y],
        *[x for y in uppi for x in y],
        *[x for y in haegri for x in y],
        *[x for y in innriPunktar for x in y]
    ]

    values, rows, cols = map(np.array, zip(*megalist))
    A = sp.coo_matrix((values, (rows, cols)), shape=(n*m, n*m)).tocsr()

    # b vector (same hack as before)
    _, vinstriNedriRows, _ = zip(*[x for y in vinstriNedri for x in y])
    vinstriNedriRows = np.array(list(set(vinstriNedriRows)))

    bValues = np.array([-2*P*hx/(L*delta*K) for _ in range(len(vinstriNedriRows))])
    columns = np.zeros(len(vinstriNedriRows))

    b = sp.coo_matrix((bValues, (vinstriNedriRows, columns)),
                      shape=(n*m, 1)).tocsr()

    sol = sp.linalg.spsolve(A, b)

    u = np.asarray(sol).reshape((n, m))
    T = u + U

    return np.max(T), hx

ns = [10, 20, 30, 40, 50, 60]
errors = []
hs = []

print("Computing reference solution...")
Tref, _ = solve_once(120)

for n in ns:
    print("n =", n)
    Tmax, h = solve_once(n)
    errors.append(abs(Tmax - Tref))
    hs.append(h)

hs = np.array(hs)
errors = np.array(errors)

# log-log fit
p, c = np.polyfit(np.log(hs), np.log(errors), 1)

print("Estimated order:", p)

plt.loglog(hs, errors, "o-")
plt.loglog(hs, np.exp(c)*hs**p, "--", label=f"slope ≈ {p:.2f}")
plt.xlabel("h")
plt.ylabel("error in Tmax")
plt.legend()
plt.grid(True, which="both")
plt.show()
