import functions as f
import scipy.sparse as sp
import time

Lx = Ly = 2
delta = 0.1
P = 5
K = 1.68
H = 0.005
U = 20
n = 200
m = 200
L = 2

breytur = [n, m, H, K, P, delta, Lx, Ly, L]

start = time.perf_counter()

innriRadir = [f.makePartOfA(*f.innriRod(*breytur, k)) for k in range(1, n-1)]

megaset = [
    # *f.makePartOfA(*f.vinstriEfri(*breytur)),
    # *f.makePartOfA(*f.vinstriNedri(*breytur)),
    # *f.makePartOfA(*f.nidri(*breytur)),
    # *f.makePartOfA(*f.uppi(*breytur)),
    # *f.makePartOfA(*f.haegri(*breytur)),
    *[x for y in innriRadir for x in y]
]    

for x in megaset:
    print(type(x))

print(len(megaset))