import time
import random
from tkinter import Tk, Canvas

from typing import Optional, TYPE_CHECKING
if TYPE_CHECKING:
    pass

class Point:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

class Line:
    def __init__(self, point1: Point, point2: Point):
        self.point1 = point1
        self.point2 = point2

    def draw(self, canvas: Canvas, fill_color: str):
        canvas.create_line(
            self.point1.x, self.point1.y,
            self.point2.x, self.point2.y,
            fill=fill_color,
            width=2
        )

class Window:
    def __init__(self, width: int, height: int):
        self.__root = Tk()
        self.__root.title("Maze Solver")
        self.__canvas = Canvas(self.__root, width=width, height=height, bg="white")
        self.__canvas.pack(fill="both", expand=True)
        self.__running = False
        self.__root.protocol("WM_DELETE_WINDOW", self.close)

    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()

    def wait_for_close(self):
        self.__running = True
        while self.__running:
            self.redraw()
        print("Window closed, application shutting down.")

    def close(self):
        self.__running = False

    def draw_line(self, line: Line, fill_color: str):
        line.draw(self.__canvas, fill_color)
    
    def get_canvas_bg(self) -> str:
        return str(self.__canvas["background"])


class Cell:
    def __init__(self, x1: int, y1: int, x2: int, y2: int, window: Optional['Window'] = None):
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self.visited = False

        self._x1 = x1
        self._y1 = y1
        self._x2 = x2
        self._y2 = y2
        self._win = window

    def draw(self):
        if self._win is None:
            return
        
        wall_color = "black"
        erased_wall_color = self._win.get_canvas_bg()

        line_left = Line(Point(self._x1, self._y1), Point(self._x1, self._y2))
        self._win.draw_line(line_left, wall_color if self.has_left_wall else erased_wall_color)

        line_right = Line(Point(self._x2, self._y1), Point(self._x2, self._y2))
        self._win.draw_line(line_right, wall_color if self.has_right_wall else erased_wall_color)

        line_top = Line(Point(self._x1, self._y1), Point(self._x2, self._y1))
        self._win.draw_line(line_top, wall_color if self.has_top_wall else erased_wall_color)

        line_bottom = Line(Point(self._x1, self._y2), Point(self._x2, self._y2))
        self._win.draw_line(line_bottom, wall_color if self.has_bottom_wall else erased_wall_color)

    def get_center(self) -> Point:
        center_x = (self._x1 + self._x2) / 2
        center_y = (self._y1 + self._y2) / 2
        return Point(int(center_x), int(center_y))

    def draw_move(self, to_cell: 'Cell', undo=False):
        if self._win is None:
            return

        center_self = self.get_center()
        center_to_cell = to_cell.get_center()
        fill_color = "gray" if undo else "red"
        move_line = Line(center_self, center_to_cell)
        self._win.draw_line(move_line, fill_color)

class Maze:
    def __init__(
        self,
        x1: int,
        y1: int,
        num_rows: int,
        num_cols: int,
        cell_size_x: int,
        cell_size_y: int,
        win: Optional['Window'] = None,
        seed: Optional[int] = None
    ):
        self._x1 = x1
        self._y1 = y1
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._win = win
        self._cells = []

        if seed is not None:
            random.seed(seed)

        self._create_cells()
        self._break_entrance_and_exit()
        
        if self._num_rows > 0 and self._num_cols > 0:
            self._break_walls_r(0, 0)
            self._reset_cells_visited()

    def _create_cells(self):
        for i in range(self._num_cols):
            col_cells = []
            for j in range(self._num_rows):
                cell_x1 = self._x1 + i * self._cell_size_x
                cell_y1 = self._y1 + j * self._cell_size_y
                cell_x2 = cell_x1 + self._cell_size_x
                cell_y2 = cell_y1 + self._cell_size_y
                new_cell = Cell(cell_x1, cell_y1, cell_x2, cell_y2, self._win)
                col_cells.append(new_cell)
            self._cells.append(col_cells)
        
        if self._win:
            for i in range(self._num_cols):
                for j in range(self._num_rows):
                    self._draw_cell(i, j)

    def _draw_cell(self, i: int, j: int):
        if self._win is None: return
        if 0 <= i < self._num_cols and 0 <= j < self._num_rows:
            self._cells[i][j].draw()
            self._animate()
    
    def _animate(self):
        if self._win is None: return
        self._win.redraw()
        time.sleep(0.02) # Adjusted sleep time for potentially faster solving animation

    def _break_entrance_and_exit(self):
        if self._num_cols == 0 or self._num_rows == 0: return
        self._cells[0][0].has_top_wall = False
        if self._win: self._draw_cell(0, 0)
        self._cells[self._num_cols - 1][self._num_rows - 1].has_bottom_wall = False
        if self._win: self._draw_cell(self._num_cols - 1, self._num_rows - 1)

    def _break_walls_r(self, start_i: int, start_j: int):
        stack = []
        current_cell = self._cells[start_i][start_j]
        current_cell.visited = True
        stack.append((start_i, start_j))
        while stack:
            i, j = stack[-1] 
            current_cell = self._cells[i][j]
            to_visit_indices = []
            # Check neighbors (left, right, up, down)
            if i > 0 and not self._cells[i-1][j].visited: to_visit_indices.append((i-1, j))
            if i < self._num_cols - 1 and not self._cells[i+1][j].visited: to_visit_indices.append((i+1, j))
            if j > 0 and not self._cells[i][j-1].visited: to_visit_indices.append((i, j-1))
            if j < self._num_rows - 1 and not self._cells[i][j+1].visited: to_visit_indices.append((i, j+1))

            if not to_visit_indices:
                if self._win: self._draw_cell(i, j) # Draw on backtrack
                stack.pop()
            else:
                next_i, next_j = random.choice(to_visit_indices)
                next_cell = self._cells[next_i][next_j]
                # Knock down walls
                if next_i == i + 1: current_cell.has_right_wall, next_cell.has_left_wall = False, False
                elif next_i == i - 1: current_cell.has_left_wall, next_cell.has_right_wall = False, False
                elif next_j == j + 1: current_cell.has_bottom_wall, next_cell.has_top_wall = False, False
                elif next_j == j - 1: current_cell.has_top_wall, next_cell.has_bottom_wall = False, False
                if self._win: self._draw_cell(i, j)
                next_cell.visited = True
                stack.append((next_i, next_j))

    def _reset_cells_visited(self):
        if self._num_cols == 0 or self._num_rows == 0: return
        for i in range(self._num_cols):
            for j in range(self._num_rows):
                self._cells[i][j].visited = False
    
    # NEW: solve method (public)
    def solve(self) -> bool:
        """
        Solves the maze starting from the top-left cell (0,0).
        Returns True if a path to the exit is found, False otherwise.
        """
        if self._num_cols == 0 or self._num_rows == 0:
            return False # Cannot solve an empty maze
        return self._solve_r(0, 0)

    # NEW: _solve_r method (recursive helper)
    def _solve_r(self, i: int, j: int) -> bool:
        """
        Recursively tries to solve the maze from cell (i,j).
        i: current column index
        j: current row index
        Returns True if this cell is or leads to the exit, False otherwise.
        """
        self._animate() # Animate each step of the solving process

        current_cell = self._cells[i][j]
        current_cell.visited = True

        # Check if current cell is the exit cell
        # Exit is at (num_cols - 1, num_rows - 1)
        if i == self._num_cols - 1 and j == self._num_rows - 1:
            return True # Reached the end

        # Explore neighbors: (order can matter for visual path, e.g., Right, Down, Left, Up)
        
        # Try to move Right
        if (i + 1 < self._num_cols and # Check bounds
            not current_cell.has_right_wall and # Check wall
            not self._cells[i+1][j].visited):   # Check if visited
            
            next_cell = self._cells[i+1][j]
            current_cell.draw_move(next_cell) # Draw forward move
            if self._solve_r(i + 1, j):
                return True
            else:
                current_cell.draw_move(next_cell, undo=True) # Draw undo move

        # Try to move Left
        if (i - 1 >= 0 and
            not current_cell.has_left_wall and
            not self._cells[i-1][j].visited):
            
            next_cell = self._cells[i-1][j]
            current_cell.draw_move(next_cell)
            if self._solve_r(i - 1, j):
                return True
            else:
                current_cell.draw_move(next_cell, undo=True)

        # Try to move Down
        if (j + 1 < self._num_rows and
            not current_cell.has_bottom_wall and
            not self._cells[i][j+1].visited):

            next_cell = self._cells[i][j+1]
            current_cell.draw_move(next_cell)
            if self._solve_r(i, j + 1):
                return True
            else:
                current_cell.draw_move(next_cell, undo=True)

        # Try to move Up
        if (j - 1 >= 0 and
            not current_cell.has_top_wall and
            not self._cells[i][j-1].visited):
            
            next_cell = self._cells[i][j-1]
            current_cell.draw_move(next_cell)
            if self._solve_r(i, j - 1):
                return True
            else:
                current_cell.draw_move(next_cell, undo=True)
        
        # If none of the directions led to the solution from this cell
        return False