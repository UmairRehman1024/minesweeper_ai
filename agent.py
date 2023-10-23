from game import MinesweeperGameAI, ROWS, COLS
import random


class AI:
    def __init__(self):
        game = MinesweeperGameAI
        self.playerGrid = game.playerGrid
        self.numOfActions = 0
        directions = {"above", "below", "left", "right"}

    def getRandomSquare(self):
        while True:
            row = random.randint(0, ROWS - 1)
            col = random.randint(0, COLS - 1)
            if not self.playerGrid.grid[row][col].revealed:
                break
        return (row, col)

    def getAction(self):

        if self.numOfActions == 0:
            #first move
            square = self.getRandomSquare()
            
        #check if there are any hidden square that are guarenteed  to be part of path, a bomb or is safe
        isPartPath, squarePath = self.checkPartPath()
        isSafe, squareSafe = self.checkSafe()
        IsBomb, squareBomb = self.checkBomb()
        
        if isPartPath:
            return squarePath
        elif isSafe:
            return squareSafe
        elif IsBomb:
            return squareBomb
        
        #check around path

        return square
    
    def checkPartPath(self):
        #check if any guarenteed part of path
        #if true return square that is part of path
        isPartPath = False
        for row in range(ROWS - 1):
            for col in range(COLS - 1):
                square = self.playerGrid[row][col]
                if square.path:

                    # if row = 0 
                    #   check left right and below
                    # elif row = Rows - 1
                    #   check left right and above
                    # elif col = 0 
                    # check above below and right
                    # elif col = COLS - 1
                    # check above below and left
                    # else 
                    #   check all directions
                    
                    if row == 0:
                        # check left right and below
                        below = self.playerGrid[row][col + 1]
                        left = self.playerGrid[row - 1][col]
                        right = self.playerGrid[row + 1][col]

                        if below.revealed and left.revealed and  not(above.path or below.path or left.path):
                            return isPartPath, right
                        elif below.revealed and right.revealed and  not(above.path or below.path or right.path):
                            return isPartPath, left
                        elif left.revealed and right.revealed and  not(above.path or left.path or right.path):
                            return isPartPath, below
                    elif row == ROWS - 1:
                        # check left right and above
                        above = self.playerGrid[row][col - 1]
                        left = self.playerGrid[row - 1][col]
                        right = self.playerGrid[row + 1][col]  

                        if above.revealed and left.revealed and  not(above.path or below.path or left.path):
                            return isPartPath, right
                        elif above.revealed and right.revealed and  not(above.path or below.path or right.path):
                            return isPartPath, left
                        elif left.revealed and right.revealed and  not(below.path or left.path or right.path):
                            return isPartPath, above


                    elif col == 0 :
                        # check above below and right
                        above = self.playerGrid[row][col - 1]
                        below = self.playerGrid[row][col + 1]
                        right = self.playerGrid[row + 1][col]


                        if above.revealed and below.revealed and not(above.path or below.path or left.path):
                            return isPartPath, right
                        elif above.revealed and right.revealed and not(above.path or left.path or right.path):
                            return isPartPath, below
                        elif below.revealed and right.revealed and not(below.path or left.path or right.path):
                            return isPartPath, above
                        
                    elif col == COLS - 1:
                        # check above below and left
                        above = self.playerGrid[row][col - 1]
                        below = self.playerGrid[row][col + 1]
                        left = self.playerGrid[row - 1][col]

                        if above.revealed and below.revealed and not(above.path or below.path or right.path):
                            return isPartPath, left
                        elif above.revealed and left.revealed and not(above.path or left.path or right.path):
                            return isPartPath, below
                        elif below.revealed and left.revealed and not(below.path or left.path or right.path):
                            return isPartPath, above
                            
                    else:
                        # check all directions
                        above = self.playerGrid[row][col - 1]
                        below = self.playerGrid[row][col + 1]
                        left = self.playerGrid[row - 1][col]
                        right = self.playerGrid[row + 1][col]
                        if above.revealed and below.revealed and left.revealed and  not(above.path or below.path or left.path):
                            return isPartPath, right
                        elif above.revealed and below.revealed and right.revealed and  not(above.path or below.path or right.path):
                            return isPartPath, left
                        elif above.revealed and left.revealed and right.revealed and  not(above.path or left.path or right.path):
                            return isPartPath, below
                        elif below.revealed and left.revealed and right.revealed and  not(below.path or left.path or right.path):
                            return isPartPath, above



    



    def checkBomb(self):
        #check if any guarenteed bombs
        #if true return square that is bomb

        pass

    def checkSafe(self):
        #check if any guarenteed safe squares
        #if true return square that is safe
        pass

