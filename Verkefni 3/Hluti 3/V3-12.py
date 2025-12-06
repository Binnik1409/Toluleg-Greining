import math as m
import functions as f
import numpy as np

T = 200
n = 10000
DIST = 0.1

epsilon = 10**(-5)

theta0 = [k*m.pi/10 for k in range(10)]
seperation_times = np.zeros((10,10))

for x in theta0:
    for y in theta0:
        y10 = [x, y, 0, 0]
        y20 = [epsilon + x, epsilon + y, 0, 0]

        pendulum1 = f.makeDoublePendulumCoords(y10, T, n-1)
        pendulum2 = f.makeDoublePendulumCoords(y20, T, n-1)
        
        for i in range(len(pendulum1[1][0])):
            lower_ball1 = pendulum1[1]
            lower_ball2 = pendulum2[1]
            if f.getDistance(lower_ball1[0][i], lower_ball1[1][i], lower_ball2[0][i], lower_ball2[1][i]) > DIST:
                seperation_times[theta0.index(x)][theta0.index(y)] = T*i/n
                print(T*i/n)
                break

print(seperation_times)
print("0 þýðir að mismunur fannst ekki á bilinu")