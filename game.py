import pygame
from CreateGrid import CreateGrid

pygame.init()

WIDTH = 640
HEIGHT = 480
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
running = True
pygame.display.set_caption("Pathfinding Minesweeper")

#create grid
ROWS = 5
COLS = 5
CELL_SIZE = 40
PADDING = 2
MAX_BOMBS = 5

grid = CreateGrid(ROWS, COLS, CELL_SIZE, PADDING, MAX_BOMBS, WIDTH, HEIGHT)


while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("purple")

 

    # RENDER YOUR GAME HERE
    for row in range(5):
        for col in range(5):
                if grid[row][col].bomb == True:
                     color = (255,0,0)
                else:
                     color = (255,255,255)
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