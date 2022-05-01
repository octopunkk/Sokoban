import pygame
import json

pygame.init()
window = pygame.display.set_mode((500, 500))
pygame.display.set_caption("Sokoban")
with open("level0.json", "r") as f:
    lvl0 = json.load(f)

"""
Lvl 0 :
# # # #
  x   #
#     #
* @   #
# # # #
Player = x
Box = @
Goal = *
Wall = #
Empty = 0
"""

RED = (255, 0, 0)  # Player
GREEN = (0, 255, 0)  # Goal
BLUE = (0, 0, 255)  # Box
WHITE = (255, 255, 255)  # Empty
BLACK = (0, 0, 0)  # Wall
BLOCKSIZE = 100


def initGrid(level):
    grid = [[0] * level["size"] for _ in range(level["size"])]
    for x, y in level["walls"]:
        grid[x][y] = "#"
    for x, y in level["boxes"]:
        grid[x][y] = "@"
    for x, y in level["goals"]:
        grid[x][y] = "*"
    player_x, player_y = level["player"]
    grid[player_x][player_y] = "x"
    return grid


def getPlayerCoordinates(grid):
    return [(index, row.index("x")) for index, row in enumerate(grid) if 'x' in row][0]


def pathIsClear(grid, destination):
    x, y = destination
    return grid[x][y] == 0 or grid[x][y] == "*"


def boxIsHere(grid, destination):
    x, y = destination
    return grid[x][y] == "@"


def levelIsComplete(grid):
    levelComplete = True
    for row in grid:
        if "*" in row:
            levelComplete = False
    return levelComplete


def movementHandler(movement, coordinates):
    x, y = coordinates
    match movement:
        case "UP":
            destination = [x - 1, y]
        case "DOWN":
            destination = [x + 1, y]
        case "LEFT":
            destination = [x, y - 1]
        case "RIGHT":
            destination = [x, y + 1]
        case _:
            destination = "Invalid movement !"
    return destination


def updateGrid(grid, movement):
    newGrid = grid
    playerCoord = getPlayerCoordinates(grid)
    destination = movementHandler(movement, playerCoord)

    if pathIsClear(grid, destination):
        newGrid[playerCoord[0]][playerCoord[1]] = 0
        newGrid[destination[0]][destination[1]] = "x"
        return newGrid
    elif boxIsHere(grid, destination):
        boxDestination = movementHandler(movement, destination)
        if pathIsClear(grid, boxDestination):
            newGrid[playerCoord[0]][playerCoord[1]] = 0
            newGrid[destination[0]][destination[1]] = "x"
            newGrid[boxDestination[0]][boxDestination[1]] = "@"
            return newGrid
    if levelIsComplete(newGrid):
        print("level complete !")
    return grid


def paintGrid(grid):
    for rowIndex, row in enumerate(grid):
        for columnIndex, column in enumerate(row):
            rectangle = pygame.Rect(columnIndex * BLOCKSIZE, rowIndex * BLOCKSIZE, BLOCKSIZE, BLOCKSIZE)
            match column:
                case "x":
                    pygame.draw.rect(window, RED, rectangle)
                    pygame.draw.rect(window, WHITE, rectangle, width=5)
                case "@":
                    pygame.draw.rect(window, BLUE, rectangle)
                    pygame.draw.rect(window, WHITE, rectangle, width=5)
                case "#":
                    pygame.draw.rect(window, BLACK, rectangle)
                    pygame.draw.rect(window, WHITE, rectangle, width=5)
                case "*":
                    pygame.draw.rect(window, GREEN, rectangle)
                    pygame.draw.rect(window, WHITE, rectangle, width=5)
                case 0:
                    pygame.draw.rect(window, WHITE, rectangle)
                    pygame.draw.rect(window, WHITE, rectangle, width=5)

            pygame.display.flip()


def main(level):
    run = True
    grid = initGrid(level)

    while run:
        pygame.time.delay(10)
        hasMoved = False
        paintGrid(grid)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            grid = updateGrid(grid, "LEFT")
            hasMoved = True
        elif keys[pygame.K_RIGHT]:
            grid = updateGrid(grid, "RIGHT")
            hasMoved = True
        elif keys[pygame.K_UP]:
            grid = updateGrid(grid, "UP")
            hasMoved = True
        elif keys[pygame.K_DOWN]:
            grid = updateGrid(grid, "DOWN")
            hasMoved = True
        if hasMoved:
            pygame.time.delay(100)
        paintGrid(grid)


main(lvl0)
