import functions as f

Lx = Ly = 2
delta = 0.1
P = 5
K = 1.68
H = 0.005
U = 20
n = 5
m = 5
L = 2

breytur = [n, m, H, K, P, delta, Lx, Ly, L]

vinstriEfriA = f.makePartOfA(*f.vinstriEfri(*breytur))
vinstriNedriA = f.makePartOfA(*f.vinstriNedri(*breytur))
nidriA = f.makePartOfA(*f.nidri(*breytur))
uppiA = f.makePartOfA(*f.uppi(*breytur))
haegriA = f.makePartOfA(*f.haegri(*breytur))


print(partA)