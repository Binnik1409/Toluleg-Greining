import math as m
import functions as f

def makeDoublePendulumCoords(y0, T, n, l1=2, l2=2):
    '''
    y0=[theta1_0, theta2_0, omega1_0, omega2_0]
    '''

    theta1, theta2, omega1, omega2 = f.RKsolverLotkaVolterra_Y4(y0, T, n, f.mjaaa)
    theta_both = [theta1,theta2]

    x1 = [l1*m.sin(theta) for theta in theta1]
    y1 = [-l1*m.cos(theta) for theta in theta1]
    x2 = [l2*m.sin(theta_both[0][i])+l2*m.sin(theta_both[1][i]) for i in range(len(theta1))]
    y2 = [-l1*m.cos(theta_both[0][i])-l2*m.cos(theta_both[1][i]) for i in range(len(theta1))]
    return ((x1, y1), (x2, y2))
    #f.make_plt([(x1, y1),(x2, y2)], theta1, filename, fps)


epsilon = 10**(-4)
y10 = [m.pi/2, m.pi/2, 0, 0]
y20 = [epsilon + m.pi/2, epsilon + m.pi/2, 0, 0]

pendulum1 = makeDoublePendulumCoords(y10, 120, 5000)
pendulum2 = makeDoublePendulumCoords(y20, 120, 5000)

f.make_multi_pendulums_plt([pendulum1, pendulum2], pendulum1[0][0], filename='multi_pendulum.mp4', fps=30)
