import numpy as np

def create_matrix_A(n, alpha, beta):
    'Creates a specific n x n matrix with given alpha value.'

    I = np.ones(n)
    b = I * beta
    I = np.ones(n-1)
    a = I * alpha
    matrix = np.diag(b) + np.diag(a,-1) + np.diag(a,1)
    matrix[0][0] = 1
    matrix[0][1] = 0
    matrix[n-1][n-2] = 0
    matrix[n-1][n-1] = 1

    return matrix

def create_vector_b(n, L, x, y0, yn):
    'Creates a specific vector b of size n with given parameters.'

    vector_b = np.zeros(n)
    for i in range(1, n-1):
        vector_b[i] = x[i]*(L - x[i])

    vector_b[0] = y0
    vector_b[-1] = yn

    return vector_b