import unittest
from window import Maze, Cell 

class Tests(unittest.TestCase):
    # ... (previous tests remain unchanged) ...
    def test_maze_create_cells_basic(self):
        num_cols = 12
        num_rows = 10
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10) 
        self.assertEqual(len(m1._cells), num_cols)
        if num_cols > 0:
            self.assertEqual(len(m1._cells[0]), num_rows)

    def test_maze_create_cells_large(self):
        num_cols = 50
        num_rows = 40
        m1 = Maze(10, 10, num_rows, num_cols, 5, 5)
        self.assertEqual(len(m1._cells), num_cols)
        if num_cols > 0:
            self.assertEqual(len(m1._cells[0]), num_rows)

    def test_maze_create_cells_single_cell(self):
        num_cols = 1
        num_rows = 1
        m1 = Maze(0, 0, num_rows, num_cols, 100, 100)
        self.assertEqual(len(m1._cells), num_cols)
        if num_cols > 0:
            self.assertEqual(len(m1._cells[0]), num_rows)
    
    def test_maze_create_cells_zero_rows(self):
        num_cols = 5
        num_rows = 0
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        self.assertEqual(len(m1._cells), num_cols)
        if num_cols > 0 and num_rows > 0:
             self.assertEqual(len(m1._cells[0]), num_rows)
        elif num_cols > 0 and num_rows == 0:
             self.assertEqual(len(m1._cells[0]), 0)


    def test_maze_create_cells_zero_cols(self):
        num_cols = 0
        num_rows = 5
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        self.assertEqual(len(m1._cells), num_cols)

    def test_maze_break_entrance_and_exit(self):
        num_cols = 10
        num_rows = 12
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        self.assertFalse(m1._cells[0][0].has_top_wall)
        exit_col_idx = num_cols - 1
        exit_row_idx = num_rows - 1
        self.assertFalse(m1._cells[exit_col_idx][exit_row_idx].has_bottom_wall)

    def test_maze_break_entrance_and_exit_1x1(self):
        num_cols = 1
        num_rows = 1
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        self.assertFalse(m1._cells[0][0].has_top_wall)
        self.assertFalse(m1._cells[0][0].has_bottom_wall)
        self.assertTrue(m1._cells[0][0].has_left_wall)
        self.assertTrue(m1._cells[0][0].has_right_wall)

    def test_all_cells_visited_after_break_walls(self):
        num_cols = 5
        num_rows = 6
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10, seed=0) 
        # _break_walls_r runs, then _reset_cells_visited runs.
        # So, after Maze init, all cells should have visited = False.
        # This test now effectively tests _reset_cells_visited.
        all_reset = True
        for i in range(num_cols):
            for j in range(num_rows):
                if m1._cells[i][j].visited: # Should be False
                    all_reset = False
                    break
            if not all_reset:
                break
        self.assertTrue(all_reset, "Not all cells had 'visited' reset to False after maze generation.")

    # NEW TEST specifically for _reset_cells_visited logic
    def test_reset_cells_visited_method(self):
        num_cols = 3
        num_rows = 3
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10, seed=1)
        
        # At this point, after __init__, all cells should have visited = False
        # due to _reset_cells_visited being called.
        for i in range(num_cols):
            for j in range(num_rows):
                self.assertFalse(m1._cells[i][j].visited, 
                                 f"Cell ({i},{j}) should have visited=False after Maze initialization.")

        # Manually set some to True to test the method directly if it were public
        # (or if we had a scenario to call it again)
        if num_cols > 0 and num_rows > 0:
            m1._cells[0][0].visited = True
            m1._cells[1][1].visited = True
            # Call the method (it's private, so for testing we'd usually test its effect via __init__)
            # If we made it public for some reason: m1.reset_cells_visited()
            # Since it's called in __init__, we are testing its effect there.
            
            # To *directly* test the method if it were callable separately:
            # 1. Set some cells to visited = True
            # m1._cells[0][0].visited = True
            # 2. Call m1._reset_cells_visited() (might need to make it public or use name mangling for test)
            # 3. Assert all are False
            # For now, the existing test_all_cells_visited_after_break_walls covers the outcome.
            # Let's refine test_all_cells_visited_after_break_walls to be more explicit about its purpose.
            pass


    # Renaming and clarifying the purpose of the previous "all_visited" test
    def test_cells_are_reset_after_generation(self):
        num_cols = 5
        num_rows = 6
        # Maze generation involves: _create_cells -> _break_entrance_and_exit -> _break_walls_r -> _reset_cells_visited
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10, seed=0) 

        for i in range(num_cols):
            for j in range(num_rows):
                self.assertFalse(m1._cells[i][j].visited, 
                                 f"Cell ({i},{j}).visited should be False after full maze initialization.")

    # Test for zero-dimension mazes and _reset_cells_visited (should not error)
    def test_reset_cells_visited_zero_dim(self):
        num_cols = 0
        num_rows = 0
        try:
            # Maze init will call _reset_cells_visited if num_rows/cols > 0
            # If num_rows/cols == 0, _reset_cells_visited has a guard.
            m1 = Maze(0, 0, num_rows, num_cols, 10, 10, seed=0)
            # Check that m1._cells is empty, confirming no cells to reset.
            self.assertEqual(len(m1._cells), 0, "Maze with zero_cols should have no cell columns.")
        except Exception as e:
            self.fail(f"_reset_cells_visited (or Maze init) failed for zero dimensions: {e}")

        num_cols = 2
        num_rows = 0
        try:
            m1 = Maze(0, 0, num_rows, num_cols, 10, 10, seed=0)
            self.assertEqual(len(m1._cells), num_cols, "Maze should have columns.")
            if num_cols > 0:
                 self.assertEqual(len(m1._cells[0]), 0, "Columns should be empty for zero_rows.")
        except Exception as e:
            self.fail(f"_reset_cells_visited (or Maze init) failed for zero rows: {e}")


if __name__ == "__main__":
    unittest.main()