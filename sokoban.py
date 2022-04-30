from tarfile import BLOCKSIZE
import pygame   
import json
import numpy as np

pygame.init()  
window = pygame.display.set_mode((500, 500)) 
pygame.display.set_caption("Sokoban")
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

RED = (255, 0, 0) # Player
GREEN = (0, 255, 0) # Goal
BLUE = (0, 0, 255) # Box
WHITE = (255, 255, 255) # Empty
BLACK = (0,0,0) # Wall
BLOCKSIZE = 100


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
  if grid[destination[0]][destination[1]]==0 or grid[destination[0]][destination[1]]=='*':
    return True
  return False

def boxIsHere(grid, destination):
  if grid[destination[0]][destination[1]]=='@':
    return True
  return False

def levelIsComplete(grid):
  levelComplete = True
  for row in grid:
    for i in row:
      if i == '*':
        levelComplete = False
  return levelComplete

def updateGrid(grid, movement):
  newGrid = grid
  playerCoord = getPlayerCoordinates(grid)
  if movement == 'UP':
    destination = [playerCoord[0]-1, playerCoord[1]]
  elif movement == 'DOWN':
    destination = [playerCoord[0]+1, playerCoord[1]]
  elif movement == 'LEFT':
    destination = [playerCoord[0], playerCoord[1]-1]
  elif movement == 'RIGHT':
    destination = [playerCoord[0], playerCoord[1]+1]
  else:
    return 'Invalid movement !'
  
  if pathIsClear(grid, destination):
    newGrid[playerCoord[0]][playerCoord[1]] = 0
    newGrid[destination[0]][destination[1]] = 'x'
    return newGrid
  elif boxIsHere(grid, destination):
    boxCoord = destination
    if movement == 'UP':
      boxDestination = [boxCoord[0]-1, boxCoord[1]]
    elif movement == 'DOWN':
      boxDestination = [boxCoord[0]+1, boxCoord[1]]
    elif movement == 'LEFT':
      boxDestination = [boxCoord[0], boxCoord[1]-1]
    elif movement == 'RIGHT':
      boxDestination = [boxCoord[0], boxCoord[1]+1]
    if pathIsClear(grid, boxDestination):
      newGrid[playerCoord[0]][playerCoord[1]] = 0
      newGrid[destination[0]][destination[1]] = 'x'
      newGrid[boxDestination[0]][boxDestination[1]] = '@'
      return newGrid
  if levelIsComplete(newGrid):
    print('level complete !')
  return grid

def paintGrid(grid):
  rowIndex = -1
  for row in grid:
    rowIndex+=1
    columnIndex = -1
    for i in row :
      columnIndex+=1
      if i == 'x':
        pygame.draw.rect(window, RED, pygame.Rect(columnIndex * BLOCKSIZE, rowIndex * BLOCKSIZE, BLOCKSIZE, BLOCKSIZE)) 
        pygame.draw.rect(window, WHITE, pygame.Rect(columnIndex * BLOCKSIZE, rowIndex * BLOCKSIZE, BLOCKSIZE, BLOCKSIZE),width=5) 
      elif i == '@':
        pygame.draw.rect(window, BLUE, pygame.Rect(columnIndex * BLOCKSIZE, rowIndex * BLOCKSIZE, BLOCKSIZE, BLOCKSIZE)) 
        pygame.draw.rect(window, WHITE, pygame.Rect(columnIndex * BLOCKSIZE, rowIndex * BLOCKSIZE, BLOCKSIZE, BLOCKSIZE),width=5) 
      elif i == '#':
        pygame.draw.rect(window, BLACK, pygame.Rect(columnIndex * BLOCKSIZE, rowIndex * BLOCKSIZE, BLOCKSIZE, BLOCKSIZE))
        pygame.draw.rect(window, WHITE, pygame.Rect(columnIndex * BLOCKSIZE, rowIndex * BLOCKSIZE, BLOCKSIZE, BLOCKSIZE),width=5) 
      elif i == '*':
        pygame.draw.rect(window, GREEN, pygame.Rect(columnIndex * BLOCKSIZE, rowIndex * BLOCKSIZE, BLOCKSIZE, BLOCKSIZE)) 
        pygame.draw.rect(window, WHITE, pygame.Rect(columnIndex * BLOCKSIZE, rowIndex * BLOCKSIZE, BLOCKSIZE, BLOCKSIZE),width=5) 
      elif i == 0:
        pygame.draw.rect(window, WHITE, pygame.Rect(columnIndex * BLOCKSIZE, rowIndex * BLOCKSIZE, BLOCKSIZE, BLOCKSIZE))
        pygame.draw.rect(window, WHITE, pygame.Rect(columnIndex * BLOCKSIZE, rowIndex * BLOCKSIZE, BLOCKSIZE, BLOCKSIZE),width=5) 

      pygame.display.flip() 

      

grid = initGrid(lvl0)

while run:
  pygame.time.delay(10) 
  hasMoved = False 
  paintGrid(grid)
  for event in pygame.event.get(): 
    if event.type == pygame.QUIT:  
        run = False
  keys = pygame.key.get_pressed() 
  if keys[pygame.K_LEFT]:
    grid = updateGrid(grid, 'LEFT')
    hasMoved = True
  elif keys[pygame.K_RIGHT]:
    grid = updateGrid(grid, 'RIGHT')
    hasMoved = True
  elif keys[pygame.K_UP]:
    grid = updateGrid(grid, 'UP')
    hasMoved = True
  elif keys[pygame.K_DOWN]:
    grid = updateGrid(grid, 'DOWN')
    hasMoved = True
  if hasMoved:
    pygame.time.delay(100) 
  paintGrid(grid)

