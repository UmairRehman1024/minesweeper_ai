import pygame
from CreateGrid import CreateGrid
from path import getPath
from numOfBombs import generateNumOfBombs

#constants
ROWS = 10
COLS = 10
CELL_SIZE = 40
PADDING = 2
MAX_BOMBS = (ROWS*COLS)*0.2
WIDTH = 640
HEIGHT = 480



# colors
hiddenColor = (255,255,255)#white
revealedColor = (150,150,150)

backgroundColor = (0,0,0)

startColor = (0,255,0)#green
endColor = (255, 154, 3)#yellowish
pathColor = (0,0,255)#blue
bombColor = (255,0,0)#red
markedBombColor = (217, 95, 24)#orange



 #pygame init
pygame.init()
font = pygame.font.Font(None, 36)

class GridSquare:

    def __init__(self, bomb, path, numOfBombs, x,y, cellSize, row, col):
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

    
# class PlayerGrid:

#     def __init__(self, rows, cols):
#         grid = [rows][cols]

class PlayerGridSquare:

    def __init__(self, row, col):
        self.revealed = False
        self.row = row
        self.col = col
        self.markedBomb =False
        self.path = False
        self.numOfBombs = -1

class PlayerGrid:
    def __init__(self):
        self.grid = [ROWS][COLS]
        for row in range(ROWS):
            for col in range(COLS):
                self.grid[row][col] = PlayerGridSquare(row, col)


    def updateSquare(self, gridSquare):
        self.grid[gridSquare.row][gridSquare.col].path = gridSquare.path
        self.grid[gridSquare.row][gridSquare.col].numOfBombs = gridSquare.numOfBombs

    def markBomb(self, row, col):
        self.grid[row][col].markedBomb = True

    
    def revealSquare(self, row, col):
        self.grid[row][col].revealed= True


        






class MinesweeperGameAI:

    def __init__(self):
        # init display
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('MineSweeperAI')
        self.clock = pygame.time.Clock()
        self.reset()
        
    def reset(self):
        self.display.fill(backgroundColor)
        self.grid, self.path, self.start, self.end = self.instanciateGrid()
        self.playerGrid = PlayerGrid()
        self.playerGrid.updateSquare(self.start)
        self.playerGrid.updateSquare(self.end)
        self.playerGrid
        self.gameOver = False
        self.win = False
        self.numOfFoundPath = 0


    def update(self):
        self.display.fill(backgroundColor)
        self.drawGrid()


    def drawGrid(self):
        for row in range(ROWS):
                for col in range(COLS):
                        square = self.grid[row][col]
                        color = hiddenColor# white
                        playerSqaure = self.playerGrid.grid[row][col]
                        
                        if square == self.start:
                            color = startColor
                            
                            #if has bombs around, show numOfBombs
                            if square.numOfBombs > 0 :
                                
                                text = self.font.render(str(square.numOfBombs), True, (0, 0, 0))
                                text_rect = text.get_rect()
                                text_rect.center = square.rect.center

                        
                        elif square == self.end:
                            color = endColor

                            #if has bombs around, show numOfBombs
                            if square.numOfBombs > 0 :
                                text = self.font.render(str(square.numOfBombs), True, (0, 0, 0))
                                text_rect = text.get_rect()
                                text_rect.center = square.rect.center


                        elif playerSqaure.revealed:
                            color = revealedColor


                            if square.bomb:
                                color = bombColor
                            if square.path:
                                color = pathColor

                            #if has bombs around and is not a bomb, show numOfBombs
                            if square.numOfBombs > 0 and square.bomb == False:
                                text = self.font.render(str(square.numOfBombs), True, (0, 0, 0))
                                text_rect = text.get_rect()
                                text_rect.center = square.rect.center
                        
                        elif playerSqaure.markedBomb:
                            color = markedBombColor


                        

                        pygame.draw.rect(self.screen, color, square.rect)


                        if square.numOfBombs > 0 and (playerSqaure.revealed or square == self.start or self.start == self.end):
                            #used to show text on top of the rect square
                            self.screen.blit(text, text_rect)
        pygame.display.flip()


    def displayText(self, text, width, height):
        text = font.render(text, True, (255, 255, 255))
        textRect = pygame.Rect(width, height, text.get_width(), text.get_height())
        self.screen.blit(text, textRect)

        
    def instanciateGrid(self):
        #instanciate grid
        grid = CreateGrid(GridSquare, ROWS, COLS, CELL_SIZE, PADDING, MAX_BOMBS, WIDTH, HEIGHT)

        # add number of bomb to each grid square
        for row in range(ROWS):
            for col in range(COLS):
                grid[row][col].set_numOfBombs(grid)

        #get the path
        path, start, end = getPath(grid, ROWS, COLS)

        return (grid, path, start, end)
    
    def play_step(self,action, square):

        # 1. update grid based on action and square chosen
        if action == 0:#mark bomb
            self.playerGrid.markBomb(square.row, square.col)
        elif action == 1:#reveal square
            self.playerGrid.revealSquare(square.row, square.col)
            self.checkGameOver(square.row, square.col)
            self.playerGrid.updateSquare(square)

        reward = 0 

        
        if self.gameOver:
            if self.win:
                reward = 50
            else:
                reward = -10
            return self.gameOver, reward
        
        if square.path:
            reward = 10

        self.update()

        self.clock.tick(60)
        # 6. return game over and score
        return self.gameOver, reward

    def checkGameOver(self, row, col):
        square = self.grid[row][col]
        if square.bomb:
            
            self.gameOver = True
            self.win = False
        else:
            if square.path:
                self.numOfFoundPath += 1
            if self.numOfFoundPath == len(self.path):
                self.gameOver = True
                self.win = True




