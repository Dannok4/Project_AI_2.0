import itertools
from pysat.solvers import Solver
from pysat.formula import CNF
from itertools import combinations


def generate_cnf(matrix):
    rows = len(matrix)
    cols = len(matrix[0])
    cnf_clauses = []

    # Helper function to add clauses
    def add_clause(clause):
        cnf_clauses.append(clause)

    # Check cells within the matrix boundaries
    def in_bounds(r, c):
        return 0 <= r < rows and 0 <= c < cols

    for i in range(rows):
        for j in range(cols):
            if isinstance(matrix[i][j], int):
                k = matrix[i][j]
                # Collect variables around the current cell that could potentially contain traps
                neighbors = []
                for di in [-1, 0, 1]:
                    for dj in [-1, 0, 1]:
                        ni, nj = i + di, j + dj
                        if (di != 0 or dj != 0) and in_bounds(ni, nj) and matrix[ni][nj] == '_':
                            neighbors.append((nj + ni * 10) if nj + ni * 10 >= 0 else (-1) * (abs(nj + ni * 10)))

                if len(neighbors) > 0:
                    # Generate "At least k" clauses: combinations of size k where at least one must be True
                    at_least_k = combinations(neighbors, k)
                    at_least_k_clauses = [list(comb) for comb in at_least_k]
                    for clause in at_least_k_clauses:
                        add_clause(clause)

                    # Generate "At most k" clauses: combinations of size k+1 where at least one must be False
                    at_most_k = combinations(neighbors, k + 1)
                    at_most_k_clauses = [[-var for var in comb] for comb in at_most_k]
                    for clause in at_most_k_clauses:
                        add_clause(clause)

    return cnf_clauses


def read_grid_from_file(filename):
    grid = []
    with open(filename, 'r') as file:
        for line in file:
            row = []
            for item in line.strip().split(','):
                if item.strip() == '_':
                    row.append('_')  # -1 đại diện cho ô trống
                else:
                    row.append(int(item.strip()))  # Chuyển các chuỗi số thành số nguyên
            grid.append(row)
    return grid

#use pysat to sovlve CNF correctly
def solve_cnf(cnf):
    solver = Solver(name='g4')
    solver.append_formula(cnf)
    if solver.solve():
        return solver.get_model()
    return None


grid_filename = r'C:\Users\paody\Desktop\Project_AI_2.0\Project_AI_2.0\input.txt'
grid = read_grid_from_file(grid_filename)
# print("Ma trận đầu vào:")
# print(grid)
def print_grid(matrix):
    for row in matrix:
        print(" ".join(map(str, row)))

# In ma trận đầu vào
print("Ma trận đầu vào:")
print_grid(grid)


print("CNF được tạo:")
cnf = generate_cnf(grid)
print(cnf)

print("Kết quả giải CNF:")
solotion = solve_cnf(cnf)
print(solotion)