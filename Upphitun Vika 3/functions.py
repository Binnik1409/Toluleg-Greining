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

