import math as m
import numpy as np
import os
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def RKsolverLotkaVolterra(y0, T, n, f):

    y = np.array(y0, dtype=float)
    h = T / n  # time step
    theta = [y0[0]]
    omega = [y0[1]]

    for i in range(n):
        k1 = f(y)
        k2 = f(y + 0.5*h*k1)
        k3 = f(y + 0.5*h*k2)
        k4 = f(y + h*k3)

        y = y + (h/6) * (k1 + 2*k2 + 2*k3 + k4)
        theta.append(y[0])
        omega.append(y[1])

    return theta, omega


def ydot(yi, L=2, g=9.81):
    return [yi[1], (-g/L)*m.sin(yi[0])]

def eulerstep(yi, h, func, L=2, g=9.81):
    return [x + h*func(yi,L,g)[i] for i,x in enumerate(yi)]

def euler(y0, T, n, L=2, g=9.81):
    h = T/n
    y = [y0]

    for i in range(n-1):
        y.append(eulerstep(y[i], h, ydot, L, g))

    theta = []
    omega = []

    for x in y:
        theta.append(x[0])
        omega.append(x[1])

    return theta, omega

def f(y):
    theta, omega = y
    g, L = 9.81, 2
    d_theta = omega
    d_omega = -(g/L)*m.sin(theta)
    return np.array([d_theta,d_omega])


def make_plt(pendulums, theta, filename='vid.mp4'):

    # pendulums = single ->[(x1, y1)] double->[(x1, y1),(x2, y2)]

    num_p = len(pendulums)      # number of pendulums: 1 or 2

    plt.close("all")
    fig = plt.figure()
    ax = fig.add_subplot(
        111, autoscale_on=False, xlim=(-3, 3), ylim=(-3, 3), aspect="equal"
    )
    plt.xlabel("Lengdareining")
    plt.ylabel("Lengdareining")
    fig.tight_layout()

    FPS_PLAY = 30

    line_objects = []
    circle_objects = []

    for i in range(num_p):
        x, y = pendulums[i]
        line, = ax.plot([0, x[0]], [0, y[0]], "b-", lw=2)
        circ = ax.add_patch(plt.Circle((x[0], y[0]), 0.1, fc="r", zorder=3))
        line_objects.append(line)
        circle_objects.append(circ)

    def init():
        for line in line_objects:
            line.set_data([], [])
        for circ in circle_objects:
            circ.center = (-1000, -1000)
        return line_objects + circle_objects

    def animate(i):

        for p in range(num_p):
            x, y = pendulums[p]

            # Rod always starts from (0,0) for each pendulum
            line_objects[p].set_data([0, x[i]], [0, y[i]])

            # Move bob
            circle_objects[p].center = (x[i], y[i])

        return line_objects + circle_objects

    anim = animation.FuncAnimation(
        fig, animate, frames=len(theta),
        interval=1000/FPS_PLAY, blit=True, init_func=init
    )

    plt.show()

    choice = input("Make video file? (Y/N): ").strip().lower()
    if choice == "y":
        Writer = animation.writers["ffmpeg"]
        writer = Writer(fps=fps, metadata=dict(artist="Me"), bitrate=1800)
        anim.save(filename, writer=writer)
        print("Saved to:", filename)
    else:
        print("Video not saved.")


def mjaaa(start, m1=1, m2=1, l1=2, l2=2, g=9.81):
    
    # start = [y1, y2, y3, y4] = [θ1, θ2, ω1, ω2]
    y1 = start[0]
    y2 = start[1]
    y3 = start[2]
    y4 = start[3]

    delta = y2-y1 # Δ = θ2 - θ1

    a = m2*l1*(y3**2)*m.sin(delta)*m.cos(delta)
    b = m2*g*m.sin(y2)*m.cos(delta)
    c = m2*l2*(y4**2)*m.sin(delta)
    d = (m1+m2)*g*m.sin(y1)
    e = (m1+m2)*l1
    f = m2*l1*((1-m.cos(2*delta))/2)
    func1 = (a+b+c-d)/(e-f)
    i = m2*l2*(y4**2)*m.sin(delta)*m.cos(delta)
    j = (m1+m2)*(g*m.sin(y1)*m.cos(delta)-l1*(y3**2)*m.sin(delta)-g*m.sin(y2))
    k = (m1+m2)*l2
    l = m2*l2*((1-m.cos(2*delta))/2)
    func2 = (-i+j)/(k-l)
    return [y3, y4, func1, func2]


def RKsolverLotkaVolterra_Y4(y0, T, n, f, m1=1, m2=1, l1=2, l2=2, g=9.81): # modified for vector y 4x1

    y = np.array(y0, dtype=float)
    h = T / n  # time step

    # y0 = [y1, y2, y3, y4] = [θ1, θ2, ω1, ω2]
    y1 = [y0[0]]
    y2 = [y0[1]]
    y3 = [y0[2]]
    y4 = [y0[3]]

    for _ in range(n):
        k1 = f(y, m1, m2, l1, l2, g)
        k2 = f(y + 0.5*h*k1, m1, m2, l1, l2, g)
        k3 = f(y + 0.5*h*k2, m1, m2, l1, l2, g)
        k4 = f(y + h*k3, m1, m2, l1, l2, g)

        y = y + (h/6) * (k1 + 2*k2 + 2*k3 + k4)
        y1.append(y[0])
        y2.append(y[1])
        y3.append(y[2])
        y4.append(y[3])

    return y1, y2, y3, y4 # θ1:list, θ2:list, ω1:list, ω2:list