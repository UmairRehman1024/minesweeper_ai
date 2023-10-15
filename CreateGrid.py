import pygame
import random





def CreateGrid(GridSquare, rows, cols, cell_size, padding, max_bombs, width, height):


   

    grid = []
    for row in range(rows):
        grid.append([])
        for col in range(cols):
            x = col * (cell_size + padding) + (((width/2)-((cell_size*cols)+(padding*cols-1))/2))
            y = row * (cell_size + padding) + 50
            grid[row].append(GridSquare(0, 0, 0, x, y, cell_size, row, col))

    # Create a set to keep track of the positions already chosen
    chosen_positions = set()


    num_bombs = 0
    

    while num_bombs < max_bombs:
        row = random.randint(0, rows - 1)
        col = random.randint(0, cols - 1)

        # Check if the position has already been chosen
        if (row, col) not in chosen_positions:
            grid[row][col].bomb = True
            chosen_positions.add((row, col))
            num_bombs += 1

    return grid

