import math as m
import numpy as np
import functions as f

# Parameters
l1 = l2 = 2
m1 = m2 = 1
T = 10
n = 1000
fps = 30

# Base Initial Condition
# [theta1, theta2, omega1, omega2]
y_base = [m.pi/2, m.pi/2, 0, 0]

epsilon = 1e-3

# Create 3 sets of initial conditions with small perturbations
y0_list = [
    y_base,
    [y_base[0] + epsilon, y_base[1], y_base[2], y_base[3]],
    [y_base[0], y_base[1] + epsilon, y_base[2], y_base[3]]
]

pendulums_data = []
theta_main = None # To control frames

print("Calculating...")

for i, y0 in enumerate(y0_list):
    print(f"Solving for pendulum {i+1}...")
    theta1, theta2, omega1, omega2 = f.RKsolverLotkaVolterra_Y4(y0, T, n, f.mjaaa)
    
    if i == 0:
        theta_main = theta1

    # Convert to coordinates
    # theta1 etc are lists
    
    # x1 = l1 * sin(theta1)
    # y1 = -l1 * cos(theta1)
    x1 = [l1*m.sin(th) for th in theta1]
    y1 = [-l1*m.cos(th) for th in theta1]

    # x2 = x1 + l2 * sin(theta2)
    # y2 = y1 - l2 * cos(theta2)
    x2 = []
    y2 = []
    for j in range(len(theta1)):
        x2_val = x1[j] + l2*m.sin(theta2[j])
        y2_val = y1[j] - l2*m.cos(theta2[j])
        x2.append(x2_val)
        y2.append(y2_val)
    
    pendulums_data.append(((x1, y1), (x2, y2)))

print("Animation starting...")
# Call the function
f.make_multi_pendulums_plt(pendulums_data, theta_main, filename='multi_pendulum.mp4', fps=fps)
