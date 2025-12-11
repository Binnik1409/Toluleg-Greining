import scipy.sparse as sp
import numpy as np
import functions as f
import matplotlib.pyplot as plt

i = np.array([0,1,1,2,3,3,4])
j = np.array([1,0,4,2,3,4,1])
gildi = np.array([1,2,4,3,-1,1,1])

a = sp.coo_matrix((gildi,(i,j)),shape=(5,5)).tocsr()
print(a.toarray())









A, b = f.build_matrix_A_b(10,10, Lx=2.0, Ly=2.0, H=0.005, K=1.68, P=5.0, delta=0.1, L_input=2.0)
plt.spy(A)
plt.show()