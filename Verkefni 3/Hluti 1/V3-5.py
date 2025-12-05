import math as m
import functions as f

#Fastar
T = 20
n = 500
L = 2

y0 = [[m.pi/12, 0],[m.pi/2, 0]]

for y0 in y0:

    theta, omega = f.RKsolverLotkaVolterra(y0, T, n, f.f)
    x = [m.sin(i)*L for i in theta]
    y = [-m.cos(i)*L for i in theta]
    anim = f.make_plt(x, y, theta)
    f.save_animation(anim,'V3-5.mp4')




