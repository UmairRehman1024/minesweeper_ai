from path import get_neighbors



def generateNumOfBombs(grid, ROWS, COLS):

    for row in range(ROWS-1):
        for col in range(COLS-1):
            neighbours = get_neighbors(grid, grid[row][col])

            for neighbour in neighbours:
                if neighbour.bomb == True:
                    grid[row][col].numOfBombs += 1





