import numpy as np
import math as m
from functions import q_E0
from functions import modifyed_bisection

v = 1*10**(-3)
r = 5*10**(-2)
L = 100
G = (m.pi*(r**4))/(8*v*L)
Q_b = 7
p0 = 0

A_val = 3.0393347909480844
B_val = -2.397952502738618
C_val = 9.09518050541516

w = 2*np.pi/24

# 100 tímapunktar
t_values = np.linspace(0, 24, 100)

p1_values = []

for t in t_values:
    target_q = q_E0(A_val, B_val, C_val, w, t)
    p1 = modifyed_bisection(target_q, G, p0, Q_b)
    p1_values.append(p1)

print('p1 gildi:')
print('  t       p1 gildi')
for i in range(len(p1_values)):
    print(f'{t_values[i]:.2f} h  {p1_values[i]:.3e} Pa')