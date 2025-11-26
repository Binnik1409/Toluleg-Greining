import numpy as np

class Vector:
    def __init__(self, vector):
        self.vector = vector
        self.size = len(vector)
    def jacobian(self):
        jacobian = [[[] for _ in range(self.size)] for _ in range(self.size)]
        for i in range(self.size):
            for j in range(self.size):
                jacobian[i][j] = [self.vector[i][j][0] * self.vector[i][j][1], self.vector[i][j][1] - 1]
        return jacobian
    def solve(self, vals):
        solved = []
        for i in range(self.size):
            temp = self.vector[i][self.size]
            for j in range(self.size):
                temp += self.vector[i][j][0] * vals[j] ** self.vector[i][j][1]
            solved.append(temp)
        return solved
    def solve_jacobian(self, vals):
        solved = [[[] for _ in range(self.size)] for _ in range(self.size)]
        for i in range(self.size):
            for j in range(self.size):
                solved[i][j] = self.jacobian()[i][j][0] * vals[j] ** self.jacobian()[i][j][1]
        return solved
    def solve_s(self, vals):
        return np.linalg.solve(self.solve_jacobian(vals), self.solve(vals))


# def vector():
#     a = [[2, 1], [2, 3], [2, 4], 3]
#     b = [[1, 2], [4, 1], [2, 1], 0]
#     c = [[4, 3], [8, 4], [0, 0], -14]
#     return [a, b, c]

# def s_func(vector, jacobian):
#     s = 0
#     for i in range(len(vector)):
#         for j in range(len(vector)):
#             s += vector[i][j] * jacobian[i][j]
#     return s

def vector():
    a = [[2, 1], [2, 3], 3]
    b = [[1, 2], [4, 1], -2]
    return [a, b]

print(vector())
print(Vector(vector()).jacobian())
print(Vector(vector()).solve([1, 2]))
print(Vector(vector()).solve_jacobian([1, 2]))

# def jacobian(vector):
#     jacobian = [[[] for _ in range(len(vector))] for _ in range(len(vector))]
#     for i in range(len(vector)):
#         for j in range(len(vector)):
#             jacobian[i][j] = [vector[i][j][0] * vector[i][j][1], vector[i][j][1] - 1]
#     return jacobian