class sudoku(object):
    import sys 
    def __init__(self, grid_size, output = sys.stdout):
        self.output = output
        self.grid_size = grid_size
        self.grid = [["-"]*9 for _ in range(grid_size**2)]

    def fill_grid(self):
        for idx_i, i in enumerate(self.grid):
            for idx_j, j in enumerate(i):
                self.grid[idx_i][idx_j] = (idx_i*self.grid_size + idx_i/self.grid_size + idx_j) % (self.grid_size**2) + 1;
        self.print_grid()
        return self.grid


    def print_grid(self):
        row_counter = 1
        for row in self.grid:
            if row_counter == 4 or row_counter == 7: print ("_" * 25)
            row.insert(3, " | ")
            row.insert(7, " | ")
            self.output.write(" ".join(map(str,row)) + "\n")
            row_counter += 1


sudoku(3).print_grid()
print "\n"
sudoku(3).fill_grid()
