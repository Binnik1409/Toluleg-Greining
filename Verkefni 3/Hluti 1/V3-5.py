import math as m
import functions as f

#Fastar
T = 20
n = 500
L = 2


y0 = [m.pi/12, 0]
sol_1= f.RKsolverLotkaVolterra(y0, T, n, f.f)
print(sol_1)

y0 = [m.pi/2, 0]
sol_2= f.RKsolverLotkaVolterra(y0, T, n, f.f)



