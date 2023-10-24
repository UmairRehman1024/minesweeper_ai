from game import MinesweeperGameAI, ROWS, COLS
import random
import pygame
import sys


class AI:
    def __init__(self):
        game = MinesweeperGameAI()
        self.playerGrid = game.playerGrid
        self.numOfActions = 0

    def getRandomSquare(self):
        while True:
            row = random.randint(0, ROWS - 1)
            col = random.randint(0, COLS - 1)
            if not self.playerGrid.grid[row][col].revealed:
                break
        return row, col

    def getAction(self):
        if self.numOfActions == 0:
            row, col = self.getRandomSquare()
            return ('reveal', row, col)  # First move

        isPartPath, squarePathRow, squarePathCol = self.findPartPath()
        isGuaranteedBomb, guaranteedBombRow, guaranteedBombCol = self.findGuaranteedBombs()
        isGuaranteedSafe, guaranteedSafeRow, guaranteedSafeCol = self.findGuaranteedSafe()

        print("hellow")


        if isPartPath:
            return ('reveal', squarePathRow, squarePathCol)
        elif isGuaranteedBomb:
            # Choose to mark a bomb if there is a guaranteed bomb
            return ('mark_bomb', guaranteedBombRow, guaranteedBombCol)
        elif isGuaranteedSafe:
            # Choose to reveal a safe square if there is a guaranteed safe square
            return ('reveal', guaranteedSafeRow, guaranteedSafeCol)

        # If no guaranteed moves, select a random unrevealed square.
        row, col = self.getRandomSquare()
        print("random")
        return ('reveal', row, col)
    
    # def checkPartPath(self):
    #     #check if any guarenteed part of path
    #     #if true return square that is part of path
    #     isPartPath = False
    #     for row in range(ROWS - 1):
    #         for col in range(COLS - 1):
    #             square = self.playerGrid[row][col]
    #             if square.path:

    #                 # if row = 0 
    #                 #   check left right and below
    #                 # elif row = Rows - 1
    #                 #   check left right and above
    #                 # elif col = 0 
    #                 # check above below and right
    #                 # elif col = COLS - 1
    #                 # check above below and left
    #                 # else 
    #                 #   check all directions
                    
    #                 if row == 0:
    #                     # check left right and below
    #                     below = self.playerGrid[row][col + 1]
    #                     left = self.playerGrid[row - 1][col]
    #                     right = self.playerGrid[row + 1][col]

    #                     if below.revealed and left.revealed and  not(above.path or below.path or left.path):
    #                         return isPartPath, right
    #                     elif below.revealed and right.revealed and  not(above.path or below.path or right.path):
    #                         return isPartPath, left
    #                     elif left.revealed and right.revealed and  not(above.path or left.path or right.path):
    #                         return isPartPath, below
    #                 elif row == ROWS - 1:
    #                     # check left right and above
    #                     above = self.playerGrid[row][col - 1]
    #                     left = self.playerGrid[row - 1][col]
    #                     right = self.playerGrid[row + 1][col]  

    #                     if above.revealed and left.revealed and  not(above.path or below.path or left.path):
    #                         return isPartPath, right
    #                     elif above.revealed and right.revealed and  not(above.path or below.path or right.path):
    #                         return isPartPath, left
    #                     elif left.revealed and right.revealed and  not(below.path or left.path or right.path):
    #                         return isPartPath, above


    #                 elif col == 0 :
    #                     # check above below and right
    #                     above = self.playerGrid[row][col - 1]
    #                     below = self.playerGrid[row][col + 1]
    #                     right = self.playerGrid[row + 1][col]


    #                     if above.revealed and below.revealed and not(above.path or below.path or left.path):
    #                         return isPartPath, right
    #                     elif above.revealed and right.revealed and not(above.path or left.path or right.path):
    #                         return isPartPath, below
    #                     elif below.revealed and right.revealed and not(below.path or left.path or right.path):
    #                         return isPartPath, above
                        
    #                 elif col == COLS - 1:
    #                     # check above below and left
    #                     above = self.playerGrid[row][col - 1]
    #                     below = self.playerGrid[row][col + 1]
    #                     left = self.playerGrid[row - 1][col]

    #                     if above.revealed and below.revealed and not(above.path or below.path or right.path):
    #                         return isPartPath, left
    #                     elif above.revealed and left.revealed and not(above.path or left.path or right.path):
    #                         return isPartPath, below
    #                     elif below.revealed and left.revealed and not(below.path or left.path or right.path):
    #                         return isPartPath, above
                            
    #                 else:
    #                     # check all directions
    #                     above = self.playerGrid[row][col - 1]
    #                     below = self.playerGrid[row][col + 1]
    #                     left = self.playerGrid[row - 1][col]
    #                     right = self.playerGrid[row + 1][col]
    #                     if above.revealed and below.revealed and left.revealed and  not(above.path or below.path or left.path):
    #                         return isPartPath, right
    #                     elif above.revealed and below.revealed and right.revealed and  not(above.path or below.path or right.path):
    #                         return isPartPath, left
    #                     elif above.revealed and left.revealed and right.revealed and  not(above.path or left.path or right.path):
    #                         return isPartPath, below
    #                     elif below.revealed and left.revealed and right.revealed and  not(below.path or left.path or right.path):
    #                         return isPartPath, above


    def findPartPath(self):
        for row in range(ROWS):
            for col in range(COLS):
                square = self.playerGrid.grid[row][col]

                if square.path:
                    revealed_neighbors = []
                    unrevealed_neighbors = []

                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            if dr == 0 and dc == 0:
                                continue

                            r, c = row + dr, col + dc

                            if 0 <= r < ROWS and 0 <= c < COLS:
                                neighbor = self.playerGrid.grid[r][c]
                                if neighbor.revealed:
                                    revealed_neighbors.append(neighbor)
                                else:
                                    unrevealed_neighbors.append(neighbor)

                    if len(revealed_neighbors) == square.numOfBombs:
                        for unrevealed in unrevealed_neighbors:
                            return True, unrevealed.row, unrevealed.col

        return False, None, None





    def findGuaranteedBombs(self):
        for row in range(ROWS):
            for col in range(COLS):
                square = self.playerGrid.grid[row][col]

                if not square.revealed:
                    unrevealed_neighbors = 0
                    unrevealed_bombs = 0

                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            if dr == 0 and dc == 0:
                                continue

                            r, c = row + dr, col + dc

                            if 0 <= r < ROWS and 0 <= c < COLS:
                                neighbor = self.playerGrid.grid[r][c]

                                if neighbor.revealed:
                                    unrevealed_neighbors += 1
                                    if neighbor.numOfBombs == -1:
                                        unrevealed_bombs += 1

                    if unrevealed_neighbors == square.numOfBombs - unrevealed_bombs:
                        return True, row, col

        return False, None, None


    def findGuaranteedSafe(self):
        for row in range(ROWS):
            for col in range(COLS):
                square = self.playerGrid.grid[row][col]

                if not square.revealed:
                    unrevealed_neighbors = 0
                    unrevealed_bombs = 0

                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            if dr == 0 and dc == 0:
                                continue

                            r, c = row + dr, col + dc

                            if 0 <= r < ROWS and 0 <= c < COLS:
                                neighbor = self.playerGrid.grid[r][c]

                                if neighbor.revealed:
                                    unrevealed_neighbors += 1
                                    if neighbor.numOfBombs == -1:
                                        unrevealed_bombs += 1

                    if square.numOfBombs == unrevealed_bombs:
                        return True, row, col

        return False, None, None




def main():
    game = MinesweeperGameAI()
    ai = AI()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        action, row, col = ai.getAction()
        if action == 'mark_bomb':
            action = 0
        elif action == 'reveal':
            action = 1
        gameOver, win = game.play_step(action, row, col)
        ai.numOfActions += 1
        print(ai.numOfActions)
        if win:
            break
        elif gameOver:
            game.reset()

    print("Game over")
    game.displayText("You Win", )

if __name__ == '__main__':
    main()