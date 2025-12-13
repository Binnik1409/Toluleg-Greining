import functions as f
import numpy as np
import matplotlib.pyplot as plt

target = 100
low, high = 0, 50

K_list = []
P_list = []
for K in range(1,5+1):
    for _ in range(40):
        mid = 0.5*(low+high)
        if np.max(f.best_cpu_placement(P=mid,K=K)) > target:
            high = mid
        else:
            low = mid

    K_list.append(K)
    P_list.append(mid)

plt.scatter(K_list,P_list,marker='o')
plt.plot(K_list,P_list)
plt.xlabel("K")
plt.ylabel("P")
plt.legend()
plt.grid(True, which="both")
plt.show()





