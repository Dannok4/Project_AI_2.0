class grid: # create grid of puzzle
    def __init__(self):
        self.size, self.cell = self.read_file('input.txt')

    def read_file(self, path):
        with open(path, 'r') as file:
            lines = file.readlines()

        size = len(lines)

        board = [[0] * size for _ in range(size)]

        for i in range(size):
            values = lines[i].strip().split(',')
            for j in range(size):
                board[i][j] = values[j]

        return size, board

    def print_result(self):
        for row in self.cell:
            print(", ".join(row))
        print()

puzzle_grid = grid()
print('input: ')
puzzle_grid.print_result()