import pygame
from CreateGrid import CreateGrid
from path import getPath
from numOfBombs import generateNumOfBombs

#constants
ROWS = 10
COLS = 10
CELL_SIZE = 40
PADDING = 2
MAX_BOMBS = 20
WIDTH = 640
HEIGHT = 480


#pygame init
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
running = True
pygame.display.set_caption("Pathfinding Minesweeper")




#
class GridSquare:

    def __init__(self, bomb, path, numOfBombs, x,y, cellSize, row, col):
        self.revealed = False
        self.bomb =bomb
        self.path = path
        self.numOfBombs = numOfBombs
        self.rect = pygame.Rect(x, y, cellSize, cellSize)
        self.row = row
        self.col = col
        self.g_cost = 0
        self.h_cost = 0
        self.parent = None

    #used for A* pathfinding algo
    def f_cost(self):
        return self.g_cost + self.h_cost
    
    def set_numOfBombs(self, grid):
        # Define the offsets for checking neighboring squares, including diagonals
        neighbors_offsets = [
            (1, 0), (-1, 0), (0, 1), (0, -1),
            (1, 1), (-1, -1), (1, -1), (-1, 1)
        ]

        for dr, dc in neighbors_offsets:
            r, c = self.row + dr, self.col + dc
            if 0 <= r < len(grid) and 0 <= c < len(grid[0]) and grid[r][c].bomb and self.bomb == False:
                self.numOfBombs += 1


#instanciate grid
grid = CreateGrid(GridSquare, ROWS, COLS, CELL_SIZE, PADDING, MAX_BOMBS, WIDTH, HEIGHT)

# add number of bomb to each grid square
for row in range(ROWS):
    for col in range(COLS):
        grid[row][col].set_numOfBombs(grid)

#get the path
path, start, end = getPath(grid, ROWS, COLS)






# colors
hiddenColor = (255,255,255)#white
revealedColor = (150,150,150)

startColor = (0,255,0)
endColor = (255, 154, 3)
pathColor = (0,0,255)
bombColor = (255,0,0)

def displayNumOfBombs(square):
    if square.numOfBombs > 0:
        font = pygame.font.Font(None, 36)
        text = font.render(str(square.numOfBombs), True, (0, 0, 0))
        text_rect = text.get_rect()
        text_rect.center = square.rect.center

        return text_rect
        

        pygame.draw.rect(screen, color, square.rect)
        screen.blit(text, text_rect)

gameOver = False

#main game loop
while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


        #event for when clicking left mouse button 
        #used to reveal squares and check if clicked on bomb
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:

            x, y = pygame.mouse.get_pos()

            for row in range(ROWS):
                for col in range(COLS):
                    square = grid[row][col]
                    if square.rect.collidepoint(x,y):
                        if square.revealed == False:
                            square.revealed = True
                        if square.bomb:
                            gameOver = True
                            for row in range(ROWS):
                                for col in range(COLS):
                                    grid[row][col].revealed = True

                        



    
    if  gameOver == False:
    
 

        # RENDER YOUR GAME HERE
        for row in range(ROWS):
            for col in range(COLS):
                    square = grid[row][col]
                    color = hiddenColor# white

                    
                    if square == start:
                        color = startColor
                        
                        #if has bombs around, show numOfBombs
                        if square.numOfBombs > 0 :
                            font = pygame.font.Font(None, 36)
                            text = font.render(str(square.numOfBombs), True, (0, 0, 0))
                            text_rect = text.get_rect()
                            text_rect.center = square.rect.center

                    
                    elif square == end:
                        color = endColor

                        #if has bombs around, show numOfBombs
                        if square.numOfBombs > 0 :
                            font = pygame.font.Font(None, 36)
                            text = font.render(str(square.numOfBombs), True, (0, 0, 0))
                            text_rect = text.get_rect()
                            text_rect.center = square.rect.center


                    elif square.revealed:
                        color = revealedColor


                        if square.bomb:
                            color = bombColor
                        if square.path:
                            color = pathColor

                        #if has bombs around and is not a bomb, show numOfBombs
                        if square.numOfBombs > 0 and square.bomb == False:
                            font = pygame.font.Font(None, 36)
                            text = font.render(str(square.numOfBombs), True, (0, 0, 0))
                            text_rect = text.get_rect()
                            text_rect.center = square.rect.center

                    

                    pygame.draw.rect(screen, color, square.rect)


                    if square.numOfBombs > 0 and (square.revealed or square == start or start == end):
                        #used to show text on top of the rect square
                        screen.blit(text, text_rect)

    else:
        #if game over


        #show full revealed grid
        for row in range(ROWS):
            for col in range(COLS):
                    square = grid[row][col]
                    color = revealedColor
                    
                    if square.bomb:
                        color = bombColor
                    if square.path:
                        color = pathColor

                    if square.numOfBombs > 0 and square.bomb == False:
                        font = pygame.font.Font(None, 36)
                        text = font.render(str(square.numOfBombs), True, (0, 0, 0))
                        text_rect = text.get_rect()
                        text_rect.center = square.rect.center

                    
                    pygame.draw.rect(screen, color, square.rect)

                    if square.numOfBombs > 0 and (square.revealed or square == start or start == end):
                        screen.blit(text, text_rect)

        #show game over text
        font = pygame.font.Font(None, 36)
        text = font.render("GAMEOVER", True, (255, 255, 255))
        screen.blit(text, (WIDTH/2-text.get_width()/2, 25))



                
                
          


    

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()


# 0,0,0,0,b
# 0,b,0,0,b
# 0,0,b,g,0
# s,0,b,0,0
# 0,b,0,0,0