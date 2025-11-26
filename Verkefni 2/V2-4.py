import numpy as np

class Vector:
    def __init__(self, vector, jacob = None):
        self.vector = vector
        self.size = len(vector)
        self.jacob = jacob
    def jacobian(self):
        if self.jacob:
            return self.jacob
        jacobian = [[[] for _ in range(self.size)] for _ in range(self.size)]
        for i in range(self.size):
            for j in range(self.size):
                if self.vector[i][j][1] == 0:
                    jacobian[i][j] = [0, 0]
                else:
                    jacobian[i][j] = [self.vector[i][j][0] * self.vector[i][j][1], self.vector[i][j][1] - 1]
        self.jacob = jacobian
        return jacobian
    def solve(self, vals):
        solved = []
        for i in range(self.size):
            temp = self.vector[i][self.size]
            for j in range(self.size):
                temp = temp + self.vector[i][j][0] * vals[j] ** self.vector[i][j][1]
            solved.append(temp)
        return solved
    def solve_jacobian(self, vals):
        solved = [[[] for _ in range(self.size)] for _ in range(self.size)]
        for i in range(self.size):
            for j in range(self.size):
                if vals[j] == 0:
                    solved[i][j] = vals[j]
                else:
                    solved[i][j] = self.jacobian()[i][j][0] * vals[j] ** self.jacobian()[i][j][1]
        return solved
    def solve_s(self, vals):
        return np.linalg.solve(self.solve_jacobian(vals), self.solve(vals))
    def print_vector(self):
        for i in range(self.size):
            for j in range(self.size):
                print(self.vector[i][j], end="  \t")
            print(self.vector[i][self.size], end="")
            print()
    def print_jacobian(self):
        for i in range(self.size):
            for j in range(self.size):
                print(self.jacobian()[i][j], end="  \t")
            print()

QB = 1
p0 = 0
p1 = 2
K = 1

vector = [
    [[1,1], [-1,1], [-1,1], [0,0], [0,0], [0,0], [0,0], [0,0], 0],
    [[0,0], [1,1], [0,0], [-1,1], [0,0], [0,0], [0,0], [0,0], QB],
    [[0,0], [0,0], [1,1], [0,0], [-1,1], [-1,1], [0,0], [0,0], 0],
    [[0,0], [0,0], [0,0], [1,1], [1,1], [0,0], [-1,1], [0,0], 0],
    [[0,0], [0,0], [0,0], [0,0], [0,0], [1,1], [1,1], [-1,1], 0],
    [[0,0], [1,2], [-1,2], [1,2], [-1,2], [0,0], [0,0], [0,0], 0],
    [[0,0], [0,0], [0,0], [0,0], [1,2], [-1/2,2], [3/2,2], [0,0], 0],
    [[1,2], [0,0], [1,2], [0,0], [0,0], [1/2,2], [0,0], [1,2], (p0-p1)/K]
]

x0 = [1,1,2,3,4,3,2,1]
Vector(vector).print_vector()
print()
Vector(vector).print_jacobian()
print()

tol = 10**(-8)
nakv = int(np.ceil(-np.log10(tol)+2))
E = tol + 1
while E > tol:
    x = x0 - Vector(vector).solve_s(x0)
    E = np.linalg.norm(x - x0)
    x0 = x
    for i in x:
        print("%.*f" % (nakv, i), end="  ")
    print()

# print(vector)
# print(Vector(vector).jacobian())
# print(Vector(vector).solve(x0))
# print(Vector(vector).solve_jacobian(x0))
# print(Vector(vector).solve_s(x0))
