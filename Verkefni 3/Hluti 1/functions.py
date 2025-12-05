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



def save_animation(anim, filename="vid.mp4", fps=30):
    
    choice = input("Make video file? (Y/N): ").strip().lower()
    if choice == "y":
        Writer = animation.writers['ffmpeg']
        writer = Writer(fps=fps, metadata=dict(artist="Me"), bitrate=1800)
        anim.save(filename, writer=writer)
        print("Saved to:", os.path.abspath(filename))
    else:
        print("Video not saved.")