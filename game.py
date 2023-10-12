import pygame
from CreateGrid import CreateGrid
from path import getPath

pygame.init()

WIDTH = 640
HEIGHT = 480
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
running = True
pygame.display.set_caption("Pathfinding Minesweeper")

#create grid
ROWS = 10
COLS = 10
CELL_SIZE = 40
PADDING = 2
MAX_BOMBS = 25


class GridSquare:

    def __init__(self,bomb, path, numOfBombs, x,y, cellSize, row, col):
        self.bomb =bomb
        self.path = path
        self.numOfBombs = numOfBombs
        self.rect = pygame.Rect(x, y, cellSize, cellSize)
        self.row = row
        self.col = col
        self.g_cost = 0
        self.h_cost = 0
        self.parent = None

    def f_cost(self):
        return self.g_cost + self.h_cost

grid = CreateGrid(GridSquare, ROWS, COLS, CELL_SIZE, PADDING, MAX_BOMBS)


for i in range(ROWS):
    for j in range(COLS):
        print(grid[i][j].row, grid[i][j].col)

print("-----------------------------")

path = getPath(grid, ROWS, COLS)

# for i in path:
#      print(i.row, i.col)


while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    # screen.fill("purple")

 

    # RENDER YOUR GAME HERE
    for row in range(ROWS):
        for col in range(COLS):
                color = (255,255,255)

                if grid[row][col].bomb == True:
                     color = (255,0,0)
                
                if grid[row][col].path == True:
                     color = (0,255,0)
                pygame.draw.rect(screen, color, grid[row][col].rect)  # Example color  (white)

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()


# 0,0,0,0,b
# 0,b,0,0,b
# 0,0,b,g,0
# s,0,b,0,0
# 0,b,0,0,0