import math as m
import functions as f

epsilons = [3, 5, 8]

for x in epsilons:
    epsilon = 10**(-x)
    y10 = [m.pi/2, m.pi/2, 0, 0]
    y20 = [epsilon + m.pi/2, epsilon + m.pi/2, 0, 0]

    pendulum1 = f.makeDoublePendulumCoords(y10, 120, 5000)
    pendulum2 = f.makeDoublePendulumCoords(y20, 120, 5000)

    f.make_multi_pendulums_plt([pendulum1, pendulum2], pendulum1[0][0], filename='V3-11_{}.mp4'.format(x), fps=30)
