import time
import pygame
import heapq
import random

# #get start pos

# start = grid[random.randint(0, ROWS - 1)][random.randint(0, COLS - 1)]


# end = grid[random.randint(0, ROWS - 1)][random.randint(0, COLS - 1)]




def astar(grid, start, end):
    open_set = []
    closed_set = set()

    open_set.append(start)

    while open_set:
        current = min(open_set, key=lambda x: x.f_cost())
        open_set.remove(current)
        closed_set.add(current)

        if current == end:
            path = []
            while current:
                path.append(current)
                current = current.parent
            return path[::-1]

        for neighbor in get_neighbors(grid, current):
            if neighbor in closed_set or neighbor.bomb:
                continue

            tentative_g_cost = current.g_cost + 1

            if neighbor not in open_set or tentative_g_cost < neighbor.g_cost:
                neighbor.g_cost = tentative_g_cost
                neighbor.h_cost = heuristic(neighbor, end)
                neighbor.parent = current

                if neighbor not in open_set:
                    open_set.append(neighbor)

    return None

def get_neighbors(grid, node):
    neighbors = []
    for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
        r, c = node.row + dr, node.col + dc
        if 0 <= r < len(grid) and 0 <= c < len(grid[0]):
            neighbors.append(grid[r][c])
    return neighbors

def heuristic(node, goal):
    return abs(node.row - goal.row) + abs(node.col - goal.col)



def getPath(grid, ROWS, COLS):
    MAX_RETRIES = 3
    retries = 0
    startRow, startCol, endRow, endCol = getStartAndEnd(grid, ROWS, COLS)

    start = grid[startRow][startCol]
    end = grid[endRow][endCol]
    while retries < MAX_RETRIES:
        

        path = astar(grid, start, end)

        # Check if there is a valid path
        if path is not None:
            break
        else:
            print("Failed to generate a valid path. Retrying...", retries)
            retries += 1  # Increment the number of retries

        if retries == MAX_RETRIES:
            print("Failed to generate a valid path after multiple retries.")
            raise Exception("Failed to generate a valid path after multiple retries.")
            break  # Exit the loop if retries are exhausted
        else:
            time.sleep(1)  # Add a delay of 1 second before retrying

    for i in path:
        i.path = True

    return (path, start, end)

def getStartAndEnd(grid, ROWS, COLS):

    found = False

    
    while found == False:
        
        rand = random.randint(1,4)


        if rand == 1:#TOP -> BOTTOM
            startRow = 0
            startCol = random.randint(0,COLS - 1)

            endRow = ROWS - 1 
            endCol = random.randint(0,COLS - 1)

        elif rand == 2: #BOTTOM -> TOP
            startRow = ROWS - 1 
            startCol = random.randint(0,COLS - 1)

            endRow = 0
            endCol = random.randint(0,COLS - 1)
        

        elif rand == 3:#LEFT -> RIGHT
            startRow = random.randint(0,ROWS - 1)
            startCol = 0

            endRow = random.randint(0,ROWS - 1)
            endCol = COLS - 1
        else: #RIGHT -> LEFT
            startRow = random.randint(0,ROWS - 1)
            startCol = COLS - 1

            endRow = random.randint(0,ROWS - 1)
            endCol = 0


        #check if grid square is bomb
        if grid[startRow][startCol].bomb == False and grid[endRow][endCol].bomb == False:
            found = True

        

    return (startRow, startCol, endRow, endCol)

        

