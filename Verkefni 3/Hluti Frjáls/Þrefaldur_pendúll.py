import math as m
import functions as f

# Fastar
l1 = l2 = l3 = 2
m1 = m2 = m3 = 1
T = 20
n = 5000

# Upphafsgildi
y0 = [m.pi/2,m.pi/2,m.pi/2, 0, 0, 0] # [θ1, θ2, θ3, ω1, ω2, ω3]


theta1, theta2, theta3, omega1, omega2, omega3 = f.RKsolver_Y6(y0, T, n, f.f3)

x1 = [l1*m.sin(theta) for theta in theta1]
y1 = [-l1*m.cos(theta) for theta in theta1]
x2 = [l1*m.sin(theta1[i])+l2*m.sin(theta2[i]) for i in range(len(theta1))]
y2 = [-l1*m.cos(theta1[i])-l2*m.cos(theta2[i]) for i in range(len(theta1))]
x3 = [l1*m.sin(theta1[i])+l2*m.sin(theta2[i])+l3*m.sin(theta3[i]) for i in range(len(theta1))]
y3 = [-l1*m.cos(theta1[i])-l2*m.cos(theta2[i])-l3*m.cos(theta3[i]) for i in range(len(theta1))]

### V3-8 ###

f.make_plt([(x1, y1),(x2, y2),(x3, y3)],theta1,'V3-þrefaldur_pendúll.mp4',30)