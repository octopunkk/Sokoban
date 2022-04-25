from sqlite3 import Row
# import pygame   
import json
from webbrowser import get 
import numpy as np


# pygame.init()  
# window = pygame.display.set_mode((600, 600)) 
# pygame.display.set_caption("Sokoban") 

run = True
with open('level0.json', 'r') as f:
  lvl0 = json.load(f)
# Lvl 0 :
    # # # # #
    #   x   #
    # #     #
    # * @   #
    # # # # #
# Player = x
# Box = @
# Goal = *
# Wall = #
# Empty = 0


def initGrid(level):
  player = level["player"]
  walls = level["walls"]
  boxes = level["boxes"]
  goals = level["goals"]
  size = level["size"]
  grid = [[0] * size for _ in range(size)]
  for wall in walls:
    grid[wall[0]][wall[1]] = "#"
  for box in boxes:
    grid[box[0]][box[1]] = "@"
  for goal in goals:
    grid[goal[0]][goal[1]] = "*"
  grid[player[0]][player[1]] = "x"
  print(grid)
  return grid

def getPlayerCoordinates(grid):
  r = -1 # row index
  for row in grid :
    r+=1
    c = -1 # column index
    for i in row :
      c+=1
      if i == 'x' :
        return [r, c]

def pathIsClear(grid, destination):
  if grid[destination[0]][destination[1]]==0:
    return True
  return False

def updateGrid(grid, movement):
  newGrid = grid
  playerCoord = getPlayerCoordinates(grid)
  if movement == 'UP':
    destination = [playerCoord[0]-1, playerCoord[1]]
  if movement == 'DOWN':
    destination = [playerCoord[0]+1, playerCoord[1]]
  if movement == 'LEFT':
    destination = [playerCoord[0], playerCoord[1]-1]
  if movement == 'RIGHT':
    destination = [playerCoord[0], playerCoord[1]+1]
  if pathIsClear(grid, destination):
    newGrid[playerCoord[0]][playerCoord[1]] = 0
    newGrid[destination[0]][destination[1]] = 'x'
    return newGrid

  return grid

grid = initGrid(lvl0)
print(grid)
updateGrid(grid,'DOWN')
print(grid)
# while run: 
#     ## do stuff
# pygame.quit() 

