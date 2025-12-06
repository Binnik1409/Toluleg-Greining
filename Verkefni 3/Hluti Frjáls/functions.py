import math as m
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def RKsolverLotkaVolterra(y0, T, n, f):

    y = np.array(y0, dtype=float)
    h = T / n  # time step
    theta = [y0[0]]
    omega = [y0[1]]

    for _ in range(n):
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


def f2(start, m1=1, m2=1, l1=2, l2=2, g=9.81):
    
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

    return np.array([y3, y4, func1, func2]) 


def RKsolver_Y4(y0, T, n, f, y_final=''): # modified for vector y 4x1

    h = T / n  # time step

    y = y0

    # y0 = [y1, y2, y3, y4] = [θ1, θ2, ω1, ω2]
    y1 = [y0[0]]
    y2 = [y0[1]]
    y3 = [y0[2]]
    y4 = [y0[3]]

    for _ in range(n):
        k1 = f(y)
        k2 = f(y + 0.5*h*k1)
        k3 = f(y + 0.5*h*k2)
        k4 = f(y + h*k3)

        y = y + (h/6) * (k1 + 2*k2 + 2*k3 + k4)
        y1.append(y[0])
        y2.append(y[1])
        y3.append(y[2])
        y4.append(y[3])
    if y_final == 'y':
        return np.array(y1[-1], y2[-1], y3[-1], y4[-1])
    else:
        return np.array([y1, y2, y3, y4]) # θ1:list, θ2:list, ω1:list, ω2:list


def RKsolver_Y6(y0, T, n, f, y_final=''): # modified for vector y 6x1

    h = T / n  # time step

    y = y0

    # y0 = [y1, y2, y3, y4, y5, y6] = [θ1, θ2, θ3, ω1, ω2, ω3]
    y1 = [y0[0]]
    y2 = [y0[1]]
    y3 = [y0[2]]
    y4 = [y0[3]]
    y5 = [y0[4]]
    y6 = [y0[5]]

    for _ in range(n):
        k1 = f(y)
        k2 = f(y + 0.5*h*k1)
        k3 = f(y + 0.5*h*k2)
        k4 = f(y + h*k3)

        y = y + (h/6) * (k1 + 2*k2 + 2*k3 + k4)
        y1.append(y[0])
        y2.append(y[1])
        y3.append(y[2])
        y4.append(y[3])
        y5.append(y[4])
        y6.append(y[5])

    if y_final == 'y':
        return np.array([y1[-1], y2[-1], y3[-1], y4[-1], y5[-1], y6[-1]])
    else:
        return np.array([y1, y2, y3, y4, y5, y6]) # θ1:list, θ2:list, θ3:list, ω1:list, ω2:list, ω3:list


def make_plt(pendulums, theta, filename='vid.mp4',fps=30,frame=5):

    num_p = len(pendulums)  # 1 or 2


    plt.close("all")
    fig = plt.figure()
    ax = fig.add_subplot(
        111, autoscale_on=False,
        xlim=(-frame, frame), ylim=(-frame, frame),
        aspect="equal"
    )
    plt.xlabel("Lengdareining")
    plt.ylabel("Lengdareining")
    fig.tight_layout()

    FPS_PLAY = 100

    line_objects = []
    circle_objects = []

    # PENDULUM 1 
    x1, y1 = pendulums[0]
    line1, = ax.plot([0, x1[0]], [0, y1[0]], "b-", lw=2)
    bob1 = ax.add_patch(plt.Circle((x1[0], y1[0]), 0.1, fc="r", zorder=3))

    line_objects.append(line1)
    circle_objects.append(bob1)

    # PENDULUM 2 
    if num_p == 2 or num_p == 3:
        x2, y2 = pendulums[1]
        line2, = ax.plot([x1[0], x2[0]], [y1[0], y2[0]], "b-", lw=2)
        bob2 = ax.add_patch(plt.Circle((x2[0], y2[0]), 0.1, fc="r", zorder=3))

        line_objects.append(line2)
        circle_objects.append(bob2)

    # PENDULUM 3 
    if num_p == 3:
        x3, y3 = pendulums[2]
        line3, = ax.plot([x2[0], x3[0]], [y2[0], y3[0]], "b-", lw=2)
        bob3 = ax.add_patch(plt.Circle((x3[0], y3[0]), 0.1, fc="r", zorder=3))

        line_objects.append(line3)
        circle_objects.append(bob3)

    def init():

        for line in line_objects:
            line.set_data([], [])
        for circ in circle_objects:
            circ.center = (-1000, -1000)
        return line_objects + circle_objects


    def animate(i):

        x1_i, y1_i = x1[i], y1[i]
        line1.set_data([0, x1_i], [0, y1_i])
        bob1.center = (x1_i, y1_i)

        if num_p == 2 or num_p ==3:
            x2_i, y2_i = x2[i], y2[i]
            line2.set_data([x1_i, x2_i], [y1_i, y2_i])
            bob2.center = (x2_i, y2_i)

        if num_p == 3:
            x3_i, y3_i = x3[i], y3[i]
            line3.set_data([x2_i, x3_i], [y2_i, y3_i])
            bob3.center = (x3_i, y3_i)

        return line_objects + circle_objects

    anim = animation.FuncAnimation(
        fig, animate, frames=len(theta),
        interval=1000/FPS_PLAY, blit=True,
        init_func=init
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

def omegaDot(theta1, theta2, omega1, omega2, m1=1, m2=1, L1=2, L2=2, g=9.81):
    delta = theta2 - theta1
    #Teljari í omega1dot, aðskilið með + eða -
    T11 = m2*L1*(omega1**2)*m.sin(delta)*m.cos(delta)
    T12 = m2*g*m.sin(theta2)*m.cos(delta)
    T13 = m2*L2*(omega2**2)*m.sin(delta)
    T14 = -(m1+m2)*g*m.sin(theta1)

    #Nefnari í omega1dot, aðskilið með + eða -
    N1 = (m1+m2)*L1
    N2 = -m2*L1*(m.cos(delta)**2)
    
    omega1dot = (T11+T12+T13+T14)/(N1+N2)

    #Teljari í omega2dot, aðskilið með + eða -
    T21 = -m2*L2*(omega2**2)*m.sin(delta)*m.cos(delta)


def f3(state, m1=1.0, m2=1.0, m3=1.0, l1=2.0, l2=2.0, l3=2.0, g=9.81):

    th1, th2, th3, w1, w2, w3 = state
    th = np.array([th1, th2, th3], dtype=float)
    w = np.array([w1, w2, w3], dtype=float)
    ls = [l1, l2, l3]
    ms = [m1, m2, m3]

    # Jacobian
    Js = []
    for r in range(3):
        J = np.zeros((2,3), dtype=float)
        for j in range(r+1):
            J[0, j] = ls[j] * m.cos(th[j])
            J[1, j] = ls[j] * m.sin(th[j])
        Js.append(J)

    M = np.zeros((3,3), dtype=float)
    for r in range(3):
        Jr = Js[r]
        M += ms[r] * (Jr.T @ Jr)

    dM = [np.zeros((3,3), dtype=float) for _ in range(3)]
    for k in range(3):
        for r in range(3):
            if k <= r:
                dJr = np.zeros((2,3), dtype=float)
                dJr[0, k] = - ls[k] * m.sin(th[k]) 
                dJr[1, k] =   ls[k] * m.cos(th[k]) 
                Jr = Js[r]
                dM_k_r = ms[r] * (dJr.T @ Jr + Jr.T @ dJr)
                dM[k] += dM_k_r

    dMdt = np.zeros((3,3), dtype=float)
    for k in range(3):
        dMdt += dM[k] * w[k]

    q_vec = np.zeros(3, dtype=float)
    for k in range(3):
        q_vec[k] = float(w @ (dM[k] @ w))

    dV = np.zeros(3, dtype=float)
    for k in range(3):
        sum_m = 0.0
        for r in range(k, 3):
            sum_m += ms[r]
        dV[k] = sum_m * g * ls[k] * m.sin(th[k])

    RHS = - (dMdt @ w - 0.5 * q_vec + dV)

    try:
        acc = np.linalg.solve(M, RHS)
    except np.linalg.LinAlgError:
        acc = np.linalg.lstsq(M, RHS, rcond=None)[0]

    return np.array([w1, w2, w3, acc[0], acc[1], acc[2]], dtype=float)
