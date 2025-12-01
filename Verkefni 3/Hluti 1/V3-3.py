import numpy as np
import math as m
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Fastar
theta_0 = m.pi/12
theta_df_0 = 0
T = 20
n = 500

# Kalla á funcrioni úr V3_2

### result = name_of_funcrion(theta_0,theta_df_0,T,n)

# hreyfi.py
# Kristinn Torfason
# 11.01.2020
#
# Þessi skrá var prófuð á Ubuntu 18.04 með Matplotlib 3.1.1, ffmpeg 3.4.6 og Python 3.7.4
#
# Athugið að ffmpeg þarf að vera sett upp á vélinni og Matplotlib þarf að
# geta fundið það.
#------------------------------------------------------------
# figure
plt.close("all")
fig = plt.figure()

# subplot
# Stilla ása
pad = 0
ax1 = fig.add_subplot(111, autoscale_on=False, xlim=(0.0-pad, 15.0+pad), ylim=(-10-
pad, 10+pad))
plt.xlabel('x [eining]')
plt.ylabel('y [eining]')

# layout to tight
fig.tight_layout()

# Ein lota
FPS = 30 # Fjöldi ramma á sek í hreyfimyndinni.

# Til að hægja á hreyfimyndinni er hægt að auka FPS og halda FPS_PLAY föstu.
FPS_PLAY = 30 # Fjöldi ramma á sek þegar við spilum hreyfimyndinna.
# Best að hafa það 30.

t_start = 0.0 # Byrjunar tími í sek
t_end = T # Enda tími í sek (Tvær lotur)

# Reikna út fjölda ramma sem þarf og stærð eins tíma skrefs.
dt = (t_end - t_start)/n

# Gögn
line_1, = ax1.plot([], [], 'b-', ms=6) # x og y
t = np.zeros(n) # Tími

# Init function
def init():
    line_1.set_data([], [])
    return line_1, # Passa að komman þarf að vera

# Teikna
def animate(i):
    # Reikna tímann
    t[i] = t_start + i*dt
    # y gildi
    y = np.sin(t[0:i])
    line_1.set_data(t[0:i], y)
    return line_1, # Passa að komman þarf að vera

anim = animation.FuncAnimation(fig, animate, frames=n, interval=1, blit=True,
repeat=False, init_func=init)

# Sýna plot gluggann
plt.show()

# Búa til skránna
Writer = animation.writers['ffmpeg']
writer = Writer(fps=FPS_PLAY, metadata=dict(artist='Me'), bitrate=1800)
anim.save('vid.mp4', writer=writer)
