def read_file(file_path):
    board = []
    with open(file_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            row = line.strip().split(',')
            board.append([int(x) if x.strip() != '_' else None for x in row])

    num_rows = len(board)
    num_cols = len(board[0]) if board else 0
    
    return board, num_rows, num_cols

def print_problem_board(board, num_rows, num_cols):
    for i in range(num_rows):
        for j in range(num_cols):
            print(board[i][j] if board[i][j] is not None else '_', end=' ')

        print()

def print_solved_board(board, num_rows, num_cols, traps, gems, variables):
    for i in range(num_rows):
        for j in range(num_cols):
            if board[i][j] is not None:
                print(board[i][j], end=' ')
            else:
                if variables[(i, j)] in traps:
                    print('T', end=' ')
                elif variables[(i, j)] in gems:
                    print('G', end=' ')

        print()