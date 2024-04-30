from CNF_pysat import *

if __name__ == '__main__':
    board, num_rows, num_cols = read_file("E:\\{HCMUS}_AfterHK1\\Nam2\\HK2\\AI\\Proj\\ProjectAI_2.0\\Project_AI_2.0\\testcases\\9x9testcase.txt")

    print("Input:")
    print_problem_board(board, num_rows, num_cols)
    print()

    variables = set_variables_for_cells(num_rows, num_cols)
    clauses = generate_CNF_from_constraint(board, num_rows, num_cols, variables)
    #print(f"CNF: {clauses}")
    traps, gems = solve_CNF(clauses)

    if not traps and not gems:
        print("No solution")
    else:
        print("Output:")
        print_solved_board(board, num_rows, num_cols, traps, gems, variables) 