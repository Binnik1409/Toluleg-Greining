import math as m
import functions as f

### V3-7 ###

# Fastar
l1 = l2 = 2
m1 = m2 = 1
T = 20
n = 250

# Upphafsgildi
y0 = [m.pi/3, m.pi/6, 0, 0] # [θ1, θ2, ω1, ω2]


theta1, theta2, omega1, omega2 = f.RKsolver_Y4(y0, T, n, f.f2)
theta_both = [theta1,theta2]

x1 = [l1*m.sin(theta) for theta in theta1]
y1 = [-l1*m.cos(theta) for theta in theta1]
x2 = [l2*m.sin(theta_both[0][i])+l2*m.sin(theta_both[1][i]) for i in range(len(theta1))]
y2 = [-l1*m.cos(theta_both[0][i])-l2*m.cos(theta_both[1][i]) for i in range(len(theta1))]


### V3-8 ###

f.make_plt([(x1, y1),(x2, y2)],theta1,'V3-8.mp4')
