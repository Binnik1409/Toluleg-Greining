import numpy as np
import matplotlib.pyplot as plt
from f import f

s = complex(-0.35342173481620454, -1.3443489177880488)
c = np.linspace(0, 30, 1000)

func = []
for j in c:
    func.append(f(s,c1 = j))

# fig, ax = plt.subplots()
# ax.plot(c, func)
# ax.grid()
# plt.show()

for i in func:
    print(i, end="\n")
