import pygame   
import json 


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


def initGrid(level):
  player = level["player"]
  walls = level["walls"]
  boxes = level["boxes"]
  goals = level["goals"]
  size = level["size"]
  grid = [0] * size * size
  for wall in walls:
    grid[wall[0] * size + wall[1]] = "#"
  for box in boxes:
    grid[box[0] * size + box[1]] = "@"
  for goal in goals:
    grid[goal[0] * size + goal[1]] = "*"
  grid[player[0] * size + player[1]] = "x"
  return grid

initGrid(lvl0)
# while run: 
#     ## do stuff
# pygame.quit() 

