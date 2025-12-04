import math as m
import numpy as np
import os
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from functions import RKsolverLotkaVolterra

def f(y):
    theta, omega = y
    g, L = 9.81, 2
    d_theta = omega
    d_omega = -(g/L)*m.sin(theta)
    return np.array([d_theta,d_omega])


T = 20
n = 500
L = 2

y0 = [m.pi/12, 0]
sol_1= RKsolverLotkaVolterra(y0, T, n, f)
theta_1 = []
for sol in sol_1:
    theta_1.append(sol[0])

x_1 = [m.sin(i)*L for i in theta_1]
y_1 = [-m.cos(i)*L for i in theta_1]

y0 = [m.pi/2, 0]
sol_2= RKsolverLotkaVolterra(y0, T, n, f)
theta_2 = []
for sol in sol_2:
    theta_2.append(sol[0])

x_2 = [m.sin(i)*L for i in theta_2]
y_2 = [-m.cos(i)*L for i in theta_2]

theta = [theta_1,theta_2]
x_y = [[x_1,y_1],[x_2,y_2]]

for i,hnit in enumerate(x_y):

    x,y = hnit[0],hnit[1]

    # figure
    plt.close("all")
    fig = plt.figure(i+1)

    # subplot
    # Stilla ása
    pad = 0
    ax1 = fig.add_subplot(111, autoscale_on=False, xlim=(0.0-pad, 15.0+pad), ylim=(-10-
    pad, 10+pad))
    plt.xlabel('x [eining]')
    plt.ylabel('y [eining]')

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

    # Init function
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
        fig, animate, frames=len(theta[i]), interval=1000/FPS_PLAY,
        blit=True, init_func=init, repeat=False
    )


    # Sýna plot gluggann
    plt.show()

    # Búa til skránna
    make = input("Make video file? (Y/N)")
    if make.lower() == "y":
        Writer = animation.writers['ffmpeg']
        writer = Writer(fps=FPS_PLAY, metadata=dict(artist='Me'), bitrate=1800)
        anim.save('./vid.mp4', writer=writer)
        print("Saved to: " + os.path.abspath('./vid.mp4'))