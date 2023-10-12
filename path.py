import pygame
from game import grid, ROWS, COLS
import random

#get start pos

start = grid[random.randint(0, ROWS - 1)][random.randint(0, COLS - 1)]


end = grid[random.randint(0, ROWS - 1)][random.randint(0, COLS - 1)]