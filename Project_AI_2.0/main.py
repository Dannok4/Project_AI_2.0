from CNF_pysat import *
def main():
    while True:
        print("Menu:")
        print("1. Test Case 5x5")
        print("2. Test Case 9x9")
        print("3. Test Case 11x11")
        print("4. Test Case 15x15")
        print("5. Test Case 20x20")
        print("6. Quit")
        
        choice = input("Enter your choice: ")

        if choice == "1":
            #5x5 testcase
            file_path = r"C:\\Users\\VTV\\OneDrive - VNU-HCMUS\\Desktop\\ProjectAI2\\Project_AI_2.0\\Project_AI_2.0\\testcases\\5x5testcase.txt"
            solve_testcase(file_path)
        elif choice == "2":
            #9x9 testcase
            file_path = r"C:\\Users\\VTV\\OneDrive - VNU-HCMUS\\Desktop\\ProjectAI2\\Project_AI_2.0\\Project_AI_2.0\\testcases\\9x9testcase.txt"
            solve_testcase(file_path)
            pass
        elif choice == "3":
            #11x11 testcase
            file_path = r"C:\\Users\\VTV\\OneDrive - VNU-HCMUS\\Desktop\\ProjectAI2\\Project_AI_2.0\\Project_AI_2.0\\testcases\\11x11testcase.txt"
            solve_testcase(file_path)
            pass
        elif choice == "4":
            #15x15 testcase
            file_path = r"C:\\Users\\VTV\\OneDrive - VNU-HCMUS\\Desktop\\ProjectAI2\\Project_AI_2.0\\Project_AI_2.0\\testcases\\13x13testcase.txt"
            solve_testcase(file_path)
            pass
        elif choice == "5":
            #20x20 testcase
            file_path = r"C:\\Users\\VTV\\OneDrive - VNU-HCMUS\\Desktop\\ProjectAI2\\Project_AI_2.0\\Project_AI_2.0\\testcases\\20x20testcase.txt"
            solve_testcase(file_path)
            pass
        elif choice == "6":
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please try again.")

def solve_testcase(file_path):
    board, num_rows, num_cols = read_file(file_path)

    print("Input:")
    print_problem_board(board, num_rows, num_cols)
    print()

    variables = set_variables_for_cells(num_rows, num_cols)
    clauses = generate_CNF_from_constraint(board, num_rows, num_cols, variables)
    traps, gems = solve_CNF(clauses)

    if not traps and not gems:
        print("No solution")
    else:
        print("Output:")
        print_solved_board(board, num_rows, num_cols, traps, gems, variables) 

if __name__ == '__main__':
    main()

