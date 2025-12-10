import scipy.sparse as sp
import numpy as np

i = np.array([0,1,1,2,3,3,4])
j = np.array([1,0,4,2,3,4,1])
gildi = np.array([1,2,4,3,-1,1,1])

a = sp.coo_matrix((gildi,(i,j)),shape=(5,5)).tocsr()
print(a.toarray())
