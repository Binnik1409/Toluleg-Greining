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


def make_plt(x, y, theta):

    # figure
    plt.close("all")
    fig = plt.figure()

    # subplot
    # Stilla ása
    pad = 0
    ax1 = fig.add_subplot(111, autoscale_on=False, xlim=(-2.5-pad, 2.5+pad), ylim=(-2.5-pad, 2.5+pad), aspect='equal')
    plt.xlabel('Lengdareining')
    plt.ylabel('Lengdareining')

    # layout to tight
    fig.tight_layout()

    FPS = 30 # Fjöldi ramma á sek í hreyfimyndinni.
    # Til að hægja á hreyfimyndinni er hægt að auka FPS og halda FPS_PLAY föstu.
    FPS_PLAY = 30 # Fjöldi ramma á sek þegar við spilum hreyfimyndinna.
    # Best að hafa það 30.

    t_start = 0.0 # Byrjunar tími í sek
    t_end = 2*2*np.pi # Enda tími í sek (Tvær lotur)

    # Reikna út fjölda ramma sem þarf og stærð eins tíma skrefs.
    n = int(np.ceil(FPS*(t_end - t_start)))
    dt = (t_end - t_start)/n

    # Gögn
    line_1, = ax1.plot(x, y, 'b-', ms=6) # x og y
    t = np.zeros(n) # Tími

    circle = ax1.add_patch(
        plt.Circle([-1000, -1000], 0.1, fc="r", zorder=3)
    )

    def init():
        line_1.set_data([], [])
        return line_1, # Passa að komman þarf að vera

    # Teikna
    def animate(i):

        # Reikna tímann
    
        line_1.set_data([0, x[i]], [0, y[i]])
        circle.center = (x[i], y[i])
        return line_1, circle # Passa að komman þarf að vera

    anim = animation.FuncAnimation(
        fig, animate, frames=len(theta), interval=1000/FPS_PLAY,
        blit=True, init_func=init, repeat=False
    )
    plt.show()

    return anim



def save_animation(anim, filename="vid.mp4", save_video=True, fps=30):
    if save_video:
        Writer = animation.writers['ffmpeg']
        writer = Writer(fps=fps, metadata=dict(artist="Me"), bitrate=1800)
        anim.save(filename, writer=writer)
        print("Saved to:", os.path.abspath(filename))
    else:
        print("Video not saved.")

def mjaaa(start, m1=1, m2=1, l1=2, l2=2, g=9.81):
    # start = [y1, y2, y3, y4] = [theta1, theta2, omega1, omega2]
    y1 = start[0]
    y2 = start[1]
    y3 = start[2]
    y4 = start[3]

    delta = y2-y1 # Δ = theta2 - theta1 = y2 - y1

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


def RKsolverLotkaVolterra_Y4(y0, T, n, f): # modified for vector y 4x1

    y = np.array(y0, dtype=float)
    h = T / n  # time step

    # y0 = [y1, y2, y3, y4] = [theta1, theta2, omega1, omega2]
    y1 = [y0[0]]
    y2 = [y0[1]]
    y3 = [y0[2]]
    y4 = [y0[3]]

    for i in range(n):
        k1 = f(y)
        k2 = f(y + 0.5*h*k1)
        k3 = f(y + 0.5*h*k2)
        k4 = f(y + h*k3)

        y = y + (h/6) * (k1 + 2*k2 + 2*k3 + k4)
        y1.append(y[0])
        y2.append(y[1])
        y3.append(y[2])
        y4.append(y[3])

    return y1, y2, y3, y4 # theta1:list, theta2:list, omega1:list, omega2:list

def omegaDot(theta1, theta2, omega1, omega2, m1=1, m2=1, L1=2, L2=2, g=9.81):
    '''
    Reiknar út hornhröðun theta 1 og theta 2 skv. jöfnuhneppi 2 í verkefnalýsingu
    Tekur inn theta 1, theta 2, omega 1 og omega 2 og skilar omega 1 og omega 2
    Massar m1 og m2 og lengdir L1 og L2 og g hafa default gildi svo óþarfi að skilgreina þau en það er hægt að breyta þeim
    '''
    delta = theta2 - theta1
    mSum = m1+m2
    sindelta = m.sin(delta)
    cosdelta = m.cos(delta)
    sincos = sindelta*cosdelta
    #Teljari í omega1dot, aðskilið með + eða -
    T11 = m2*L1*(omega1**2)*sincos
    T12 = m2*g*m.sin(theta2)*cosdelta
    T13 = m2*L2*(omega2**2)*sindelta
    T14 = -mSum*g*m.sin(theta1)

    #Nefnari í omega1dot, aðskilið með + eða -
    N11 = mSum*L1
    N12 = -m2*L1*(cosdelta**2)
    
    omega1dot = (T11+T12+T13+T14)/(N11+N12)

    #Teljari í omega2dot, aðskilið með + eða -
    T21 = -m2*L2*(omega2**2)*sincos
    T22 = mSum*g*m.sin(theta1)*cosdelta
    T23 = -mSum*L1*(omega1**2)sindelta
    T24 = -mSum*g*m.sin(theta2)

    #Nefnari í omega2dot, aðskilið með + eða -
    N21 = mSum*L2
    N22 = -m2*L2*(cosdelta**2)

    omega2dot = (T21+T22+T23+T24)/(N21+N22)

    return omega1dot, omega2dot