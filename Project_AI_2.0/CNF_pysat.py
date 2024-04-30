from read_print_board import *
from pysat.formula import *
from itertools import combinations
from pysat.solvers import Solver

# -var represents for traps
# var represents for gems

def set_variables_for_cells(num_rows, num_cols): # set variable for each cell
    count = 1
    var = {}
    for i in range(num_rows):
        for j in range(num_cols):
            var[(i, j)] = count
            count += 1
    return var

def get_neighbors(board, pos, num_rows, num_cols): # get surrounding cells which doesn't have number
    neighbors = []
    for i in range(pos[0] - 1, pos[0] + 2):
        for j in range(pos[1] - 1, pos[1] + 2):
            if i >= 0 and i < num_rows and j >= 0 and j < num_cols and (i, j) != pos and board[i][j] is None:
                neighbors.append((i, j))
    return neighbors

def get_numbered_cells(board, num_rows, num_cols): # get cells having number
    numbered_cells = []
    for i in range(num_rows):
        for j in range(num_cols):
            if board[i][j] is not None:
                numbered_cells.append((i, j))
    return numbered_cells

def get_irrelevant_cells(board, num_rows, num_cols):
    irrelevant_cells = []

    for i in range(num_rows): # get None cells
        for j in range(num_cols):
            if board[i][j] is None:
                irrelevant_cells.append((i, j))

    new_list = irrelevant_cells.copy()

    for cell in irrelevant_cells:
        check = True

        for i in range(cell[0] - 1, cell[0] + 2): # check around cells of None cells
            for j in range(cell[1] - 1, cell[1] + 2):
                if i >= 0 and i < num_rows and j >= 0 and j < num_cols and board[i][j] is not None and (i, j) != cell:
                    new_list.remove(cell)
                    check = False
                    break

            if check == False:
                break

    return new_list

def classify_cells_based_on_combinations(combination, neighbor_cells, variables): # classify surrounding cells in or not in combinations
    not_in_cells = [] # gems cells
    in_cells = [] # traps cells

    for cell in neighbor_cells:
        if cell not in combination:
            not_in_cells.append(variables[cell])
        else:
            in_cells.append(variables[cell])

    return not_in_cells, in_cells

def generate_CNF_by_constraint_cells(cell, board, num_rows, num_cols, variables):
    clauses = []
    neighbor_cells = get_neighbors(board, cell, num_rows, num_cols)

    if board[cell[0]][cell[1]] == len(neighbor_cells): # all arounding cells are traps
        for c in neighbor_cells:
            clauses.append([-variables[c]])

        return clauses
    
    combination = combinations(neighbor_cells, board[cell[0]][cell[1]]) # get combinations from cells (all cells in combination will be considered as traps)

    for c in combination:
        not_in_cells, in_cells = classify_cells_based_on_combinations(c, neighbor_cells, variables)
        
        for cell in not_in_cells: # cells not considered as traps (considers as gems)
            sub_clause = []
            sub_clause.append(cell)
            sub_clause.extend(in_cells)
            sub_clause = sorted(sub_clause)

            if sub_clause not in clauses:
                clauses.append(sub_clause)

        for cell in in_cells: # cells considered as traps
            sub_clause = []
            sub_clause.append(-cell)
            sub_clause.extend(-x for x in not_in_cells) # get -vars from vars
            sub_clause = sorted(sub_clause)

            if sub_clause not in clauses:
                clauses.append(sub_clause)
                
    return clauses

def remove_duplicated_clauses(clauses):
    result_clauses = []

    for clause in clauses:
        if clause not in result_clauses:
            result_clauses.append(clause)

    return result_clauses

def generate_CNF_from_constraint(board, num_rows, num_cols, variables):
    clauses = []
    numbered_cells = get_numbered_cells(board, num_rows, num_cols)

    for cell in numbered_cells: # create CNF by constraint cells
        clause = generate_CNF_by_constraint_cells(cell, board, num_rows, num_cols, variables)
        clauses.extend(clause)

    # irrelevant_cells = get_irrelevant_cells(board, num_rows, num_cols)

    # for cell in irrelevant_cells:
    #     clauses.append([variables[cell]])

    clauses = remove_duplicated_clauses(clauses)

    return clauses

def solve_CNF(clauses):
    solver = Solver()
    for clause in clauses:
        solver.add_clause(clause)
    solver.solve()
    model = solver.get_model()
    if model is None:
        return [], []
    traps = []
    gems = []
    for m in model:
        if m > 0:
            gems.append(m)
        else:
            traps.append(-m)
    return traps, gems