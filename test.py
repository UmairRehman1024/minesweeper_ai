import torch 

ROWS = 8
COLS = 8

#3 channels 
#1 for revealed or not
#2 for number of bombs around the square
#3 for path or not
playerGrid = game.playerGrid


revealed, bombs, path = torch.zeros(ROWS, COLS)

for row in range(ROWS):
    for col in range(COLS):
         
        square = playerGrid.grid[row][col]

        if square.revealed:

            revealed[row][col] = 1

        bombs[row][col] = square.numOfBombs


        if square.path and square.revealed:
            path[row][col] = 1  # Square is part of the path

        
test = torch.tensor([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]).reshape(3,5)
print(test)

# when the chanels are combined, it removes the information about the rows and columns 
# need a way to have multiple channels and keep the information about the rows and columns




