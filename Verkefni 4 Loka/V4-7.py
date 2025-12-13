import functions as f
import numpy as np

target = 100
low, high = 0, 50

for _ in range(40):
    mid = 0.5*(low+high)
    if np.max(f.best_cpu_placement(P=mid)) > target:
        high = mid
    else:
        low = mid

print("Max allowed power P =", "{:.2f}".format(mid),"[W]")


