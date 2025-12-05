import math as m
import functions as f


# Fastar
y0 = [m.pi/2, 0]
T = 20
n = 500
L=2

theta, omega = f.euler(y0,T,n)

x = [m.sin(i)*L for i in theta]
y = [-m.cos(i)*L for i in theta]

anim = f.make_plt(x,y,theta)

f.save_animation_prompt(anim)
