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
                if self.vector[i][j][1] == 2:
                    temp += self.vector[i][j][0] * vals[j] * abs(vals[j])
                else:
                    temp += self.vector[i][j][0] * vals[j] ** self.vector[i][j][1]
            solved.append(temp)
        return solved
    def solve_jacobian(self, vals):
        solved = [[[] for _ in range(self.size)] for _ in range(self.size)]
        for i in range(self.size):
            for j in range(self.size):
                if vals[j] == 0:
                    solved[i][j] = vals[j]
                elif vals[j] == 1:
                    solved[i][j] = self.jacobian()[i][j][0] * abs(vals[j])
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

QB = 7
p0 = 0
p1 = 4.2*10**6
K = 1.62*10**8

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

Vector(vector).print_vector()
print()
Vector(vector).print_jacobian()
print()

# x0 = [30,7,23,14,-3,26,11,37]
x0 = [1,1,1,1,1,1,1,1]

tol = 10**(-8)
nakv = int(-np.log10(tol)+2)

E = tol + 1
j = 0
while E > tol:
    x = x0 - Vector(vector).solve_s(x0)
    E = np.linalg.norm(x - x0)
    x0 = x
    for i in x:
        print("%.*f" % (nakv, i), end="  ")
    print()
    j += 1
    if j > 10:
        break

# print(vector)
# print(Vector(vector).jacobian())
# print(Vector(vector).solve(x0))
# print(Vector(vector).solve_jacobian(x0))
# print(Vector(vector).solve_s(x0))
