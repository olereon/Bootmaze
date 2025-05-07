# main.py
from window import Window, Maze 

def main():
    screen_width = 800
    screen_height = 600
    margin = 50

    win = Window(screen_width, screen_height)

    num_cols = 15 
    num_rows = 12
    
    cell_size_x = (screen_width - 2 * margin) // num_cols
    cell_size_y = (screen_height - 2 * margin) // num_rows
    
    # Use a seed for consistent maze generation during testing/dev
    # maze = Maze(margin, margin, num_rows, num_cols, cell_size_x, cell_size_y, win, seed=0) 
    # For a random maze:
    maze = Maze(margin, margin, num_rows, num_cols, cell_size_x, cell_size_y, win, seed=None)


    # NEW: Call solve() on the maze
    print("Attempting to solve the maze...")
    if maze.solve():
        print("Maze solved!")
    else:
        print("Could not solve the maze (no path found or error).")


    win.wait_for_close()

if __name__ == "__main__":
    main()