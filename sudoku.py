import sys
import re

class Sudoku(object):
    def __init__(self, grid_size, output = sys.stdout, _input = sys.stdin):
        self.output = output
        self._input = _input
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
            if row_counter == 4 or row_counter == 7: self._print("_" * 25)
            line = row[0:3] + [" | "] + row[3:6] + [" | "] + row[6:]
            self._print(*line)
            row_counter += 1

    def _print(self, *string):
        print >> self.output, " ".join(map(str, string))

    def accept_input(self):
        while True:
            value = self._input.readline().strip()
            if re.match("ex|qu(?=it)", value, re.I):
                self._print("Goodbye!!!, thanks for playing Sudoku")
                break
            elif not re.match("\d:\d:\d",value):
                self._print("Supply input in the form x:y:value, where x and y are coordinates")
            else:
                x,y,val = value.split(":")
                self._print(x,y,val)
                self.grid[int(x) - 1][int(y) - 1] = val
                self.print_grid()

s = Sudoku(3)
s.fill_grid()
#sudoku(3).print_grid()
print "\n"
s.accept_input()
