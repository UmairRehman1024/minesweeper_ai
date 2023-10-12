import pygame
import random



class GridSquare:

    def __init__(self,bomb, path, numOfBombs, x,y, cellSize):
        self.bomb =bomb
        self.path = path
        self.numOfBombs = numOfBombs
        self.rect = pygame.Rect(x, y, cellSize, cellSize)


def CreateGrid(rows, cols, cell_size, padding, max_bombs, screenWidth, screenHeight):


   

    grid = []
    for row in range(rows):
        grid.append([])
        for col in range(cols):
            x = col * (cell_size + padding) + (100)
            y = row * (cell_size + padding) + (100)
            grid[row].append(GridSquare(0, 0, 0, x, y, cell_size))

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

