import json

import pygame

pygame.init()
window = pygame.display.set_mode((700, 700))
pygame.display.set_caption("Sokoban")
with open("levels/microban_0.json", "r") as f:
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
player + goal = .


actions : 
left:           0
down:           1
right:          2
up:             3
push_box_left:  4
push_box_down:  5
push_box_right: 6
push_box_up:    7 
"""

int_to_input = {0:"LEFT", 1:"DOWN", 2:"RIGHT", 3:"UP", 4:"LEFT", 5:"DOWN", 6:"RIGHT", 7:"UP",}


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
    player_pos = [(index, row.index("x")) for index, row in enumerate(grid) if 'x' in row]
    if player_pos == []:
        player_pos = [(index, row.index(".")) for index, row in enumerate(grid) if '.' in row][0]
    else:
        player_pos = player_pos[0]
    return player_pos


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
        if grid[playerCoord[0]][playerCoord[1]] == ".":
            newGrid[playerCoord[0]][playerCoord[1]] = "*"
        else:
            newGrid[playerCoord[0]][playerCoord[1]] = 0
        if grid[destination[0]][destination[1]] == "*":
            newGrid[destination[0]][destination[1]] = "."
        else:
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
                case ".":
                    pygame.draw.rect(window, RED, rectangle)
                    pygame.draw.rect(window, WHITE, rectangle, width=5)

            pygame.display.flip()


def gameStep(grid, keys, hasMoved):
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
    reward = getReward(grid, lvl0)
    return grid, hasMoved, reward


def simulateStep(grid, key):
    match key:
        case "LEFT":
            grid = updateGrid(grid, "LEFT")
        case "DOWN":
            grid = updateGrid(grid, "DOWN")
        case "RIGHT":
            grid = updateGrid(grid, "RIGHT")
        case "UP":
            grid = updateGrid(grid, "UP")
    return grid


def computeState(grid):
    state = []
    for row in grid:
        state += row
    return state


def computeActions(grid):
    all_movements = ["LEFT", "DOWN", "RIGHT", "UP"]
    possible_movements = []
    playerCoord = getPlayerCoordinates(grid)
    for index, move in enumerate(all_movements):
        destination = movementHandler(move, playerCoord)
        if pathIsClear(grid, destination):
            possible_movements.append(index)
        elif boxIsHere(grid, destination):
            match move:
                case "LEFT":
                    possible_movements.append(4)
                case "DOWN":
                    possible_movements.append(5)
                case "RIGHT":
                    possible_movements.append(6)
                case "UP":
                    possible_movements.append(7)
    return possible_movements


def futurePossibleStates(grid):
    actions = computeActions(grid)
    start_state = computeState(grid)
    states = []
    for action in actions:
        states.append(computeState(simulateStep(grid, action)))
    return [(action, state) for action, state in zip(actions, states)]


def getReward(grid, current_board):
    init_goals = len(current_board['goals'])
    levelComplete = 0
    left_goals = 0
    for row in grid:
        if "*" in row:
            left_goals += 1
    if left_goals == 0:
        levelComplete = 1
    return 1 + levelComplete*10 + (init_goals - left_goals)*5


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
        grid, hasMoved, _ = gameStep(grid, keys, hasMoved)
        paintGrid(grid)


if __name__ == "__main__":
    main(lvl0)
