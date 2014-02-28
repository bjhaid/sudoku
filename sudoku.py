import sys
import re

class Grid(object):
    def __init__(self,size):
        self._size = size
        self.inner = 0
        self._grid = [["_"]*(size ** 2) for _ in range(9)]

    def __getitem__(self, coord):
        x,y = map(int,coord)
        return self._grid[x - 1][y - 1]

    def __setitem__(self, coord, value):
        x,y = map(int,coord)
        self._grid[x - 1][y - 1] = value

    def __iter__(self):
        return iter(self._grid)

    def cell(self, *coord):
        x,y = map(int,coord)
        return self[x,y]

    def row(self, *coord):
        x,y = map(int,coord)
        return self._grid[x - 1]

    def inner_grid(self, *coord):
        x,y = map(int,coord)
        def f(v):
            div,mod = divmod(v,self._size)
            if mod:
                return div * self._size
            else:
                return (div - 1) * self._size
        starting_x_index = f(x)
        ending_x_index = f(x) + self._size
        starting_y_index = f(y)
        ending_y_index = f(y) + self._size
        return [ self._grid[i][j] for i in range(starting_x_index,ending_x_index) for j in range(starting_y_index,ending_y_index) ]

    def column(self, *coord):
        x,y = map(int,coord)
        return map(lambda f: f[y -1], self._grid)

    def valid(self,value,x,y):
        return self._valid_for_row(value,x,y) and self._valid_for_column(value,x,y) and self._valid_for_inner_grid(value,x,y)

    def _valid_for_row(self,value,x,y):
        return value not in self.row(x,y)

    def _valid_for_column(self,value,x,y):
        return value not in self.column(x,y)

    def _valid_for_inner_grid(self,value,x,y):
        return value not in self.inner_grid(x,y)

    @property
    def length(self):
        return len(self._grid)

    def sample_filled_grid(self):
        for idx_i, i in enumerate(self):
            for idx_j, j in enumerate(i):
                x_i, x_j = (idx_i + 1), (idx_j + 1)
                self[x_i,x_j] = (x_i*self._size + x_i/self._size + x_j) % (self.length) + 1;
        return self._grid

class Sudoku(object):
    def __init__(self, grid_size, output = sys.stdout, _input = sys.stdin):
        self.output = output
        self._input = _input
        self.grid_size = grid_size
        self.grid = Grid(grid_size)

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
                if not self.grid.valid(val,x,y):
                    self._print(val, " is not valid for the cell")
                    continue
                self.grid[x,y] = val
                self.print_grid()

g = Grid(3)
s = Sudoku(3)
s.print_grid()
#print "\\n"
s.accept_input()
