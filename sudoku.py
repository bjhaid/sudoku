import sys
import re

class Cell(object):
    def __init__(self, x,y,value):
        x,y,value = map(int, (x,y,value))
        self._x = x
        self._y = y
        self._value = value

    def __str__(self):
        if self.value:
            return str(self.value)
        else:
            return "_"

    def __eq__(self,value):
        return self.value == value.value

    def __non__zero(self):
        return not not self.value

    def isEmpty(self):
        return (not self.value)

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def value(self):
        return self._value

class Grid(object):
    def __init__(self,size):
        self._size = size
        self.inner = 0
        self._grid = [ [Cell(i,j,0) for i in range(1, size ** 2 + 1)] for j in range(1, size ** 2 + 1)]

    def __getitem__(self, coord):
        x,y = map(int,coord)
        return self._grid[x - 1][y - 1]

    def __setitem__(self, coord, value):
        x,y = map(int,coord)
        value = int(value)
        cell = Cell(x,y,value)
        self._grid[x - 1][y - 1] = cell

    def __iter__(self):
        return iter(self._grid)

    def row(self, x):
        return self._grid[x - 1]

    def inner_grid(self, *coord):
        x,y = coord
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

    def column(self, y):
        return map(lambda f: f[y -1], self._grid)

    def valid(self,value,x,y):
        cell = Cell(x,y,value)
        return self._valid_for_row(cell) and self._valid_for_column(cell) and self._valid_for_inner_grid(cell)

    def _valid_for_row(self,cell):
        return cell not in self.row(cell.x)

    def _valid_for_column(self,cell):
        return cell not in self.column(cell.y)

    def _valid_for_inner_grid(self,cell):
        return cell not in self.inner_grid(cell.x,cell.y)

    def flatten(self):
        return [ j for i in self._grid for j in i ]

    @property
    def length(self):
        return len(self._grid)

    @property
    def isfilled(self):
        return all(map(lambda cell: cell.value, self.flatten()))

    def emptyCells(self):
        return filter(lambda cell: cell.isEmpty(), self.flatten())

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
        self._possible_values = range(1,grid_size ** 2 + 1)
        self.grid_size = grid_size
        self.grid = Grid(grid_size)

    def set_grid(self,arr):
        for i in range(len(arr)):
            for j in range(len(arr)):
                self.grid[i+1, j+1] = arr[i][j]

    def print_grid(self):
        row_counter = 1
        for row in self.grid:
            if row_counter == self.grid_size + 1 or row_counter == (self.grid_size * 2) + 1: self._print("_" * 25)
            line = row[0:self.grid_size] + [" | "] + row[self.grid_size:self.grid_size * 2] + [" | "] + row[self.grid_size * 2:]
            self._print(*line)
            row_counter += 1

    def _print(self, *string):
        print >> self.output, " ".join(map(str, string))

    def accept_input(self):
        while True:
            value = self._input.readline().strip()
            if re.match("^(ex|qu)it$", value, re.I):
                self._print("Goodbye!!!, thanks for playing Sudoku")
                break
            elif re.match("solve", value, re.I):
                self.solve()
            elif not re.match("[1-9]:[1-9]:[1-9]",value):
                self._print("Supply input in the form x:y:value, where x and y are coordinates")
            else:
                x,y,val = value.split(":")
                self._print(x,y,val)
                if not self.grid.valid(val,x,y):
                    self._print(val, " is not valid for the cell")
                    continue
                self.grid[x,y] = val
                self.print_grid()

    def solve(self):
        loop_count = len(self.grid.emptyCells())
        while not self.grid.isfilled:
            if loop_count == 0:
                self._print("Unsolvable")
                break
            max = self.grid_size ** 2 + 1
            for cell in self.grid.emptyCells():
                if not len(filter(lambda i: self.grid.valid(i,cell.x, cell.y), range(1,max))) > 1:
                    for i in range(1,max):
                        if self.grid.valid(i,cell.x,cell.y):
                            self.grid[cell.x,cell.y] = i
            loop_count -= 1


        self.print_grid()

s = Sudoku(3)
# s.set_grid([
#     [9,1,0,7,0,0,0,0,0],
#     [0,3,2,6,0,0,0,8,0],
#     [0,0,7,0,8,0,9,0,0],
#     [0,8,6,0,3,0,1,7,0],
#     [3,0,0,0,0,0,0,0,6],
#     [0,5,1,0,2,0,8,4,0],
#     [0,0,9,0,5,0,3,0,0],
#     [0,2,0,3,0,1,4,9,0],
#     [0,0,0,0,0,2,0,6,1]])

s.print_grid()
#print "\\n"
s.accept_input()
