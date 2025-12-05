import functions as f
import math as m
import matplotlib.pyplot as plt

n = 6400
T = 20
y0 = [m.pi-0.2,m.pi,0,0]

theta1,theta2,omega1,omega2 = f.RKsolverLotkaVolterra_Y4(y0, T, n, f.mjaaa)

plt.figure(figsize=(8,6))
plt.plot(theta1, theta2, color='blue')
plt.xlabel(r'$\theta_1$ (rad)')
plt.ylabel(r'$\theta_2$ (rad)')
plt.title('Stikaður ferill fyrir tvöfaldan pendúl')
plt.grid(True)
plt.show()

