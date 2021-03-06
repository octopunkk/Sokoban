import json
import pygame
import copy
from math import dist

"""
Lvl 0 :
# # # #
  x   #
#     #
* @   #
# # # #
Player = 9
Box = 1
Goal = 2
Wall = 3
Empty = 0
player + goal = 4
goal + box = 5


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

int_to_input = {0: "LEFT", 1: "DOWN", 2: "RIGHT", 3: "UP", 4: "LEFT", 5: "DOWN", 6: "RIGHT", 7: "UP"}


RED = (255, 0, 0)  # Player
GREEN = (0, 255, 0)  # Goal
BLUE = (0, 0, 255)  # Box
WHITE = (255, 255, 255)  # Empty
BLACK = (0, 0, 0)  # Wall
CYAN = (0, 128, 128)  # Box + goal
YELLOW = (255, 255, 0)  # Player + Goal
BLOCKSIZE = 100


class Sokoban():
    grid = []
    current_level = ""
    list_level = []
    window = None
    count_move = 0

    def __init__(self, list_level) -> None:
        self.list_level = list_level
        pygame.init()
        self.window = pygame.display.set_mode((700, 700))
        pygame.display.set_caption("Sokoban")

    def nextLevel(self):
        if len(self.list_level) > 0:
            with open(self.list_level.pop(), "r") as f:
                self.current_level = json.load(f)
            return True
        else:
            return False

    def initGrid(self):
        self.grid = [[0] * self.current_level["size"] for _ in range(self.current_level["size"])]
        for x, y in self.current_level["walls"]:
            self.grid[x][y] = 3
        for x, y in self.current_level["boxes"]:
            self.grid[x][y] = 1
        for x, y in self.current_level["goals"]:
            if self.grid[x][y] == 1:
                self.grid[x][y] = 5
            else:
                self.grid[x][y] = 2
        player_x, player_y = self.current_level["player"]
        self.grid[player_x][player_y] = 9
        self.count_move = 0

    def getPlayerCoordinates(self):
        player_pos = [(index, row.index(9)) for index, row in enumerate(self.grid) if 9 in row]
        if player_pos == []:
            player_pos = [(index, row.index(4)) for index, row in enumerate(self.grid) if 4 in row][0]
        else:
            player_pos = player_pos[0]
        return player_pos

    def pathIsClear(self, destination):
        x, y = destination
        return self.grid[x][y] == 0 or self.grid[x][y] == 2

    def boxIsHere(self, destination):
        x, y = destination
        return self.grid[x][y] in (1, 5)

    def levelIsComplete(self, newgrid):
        levelComplete = True
        for row in newgrid:
            if 2 in row:
                levelComplete = False
            elif 4 in row:
                levelComplete = False
        return levelComplete

    def levelIsLost(self, newgrid):
        levelLost = False
        lost_cube = 0
        for index_row, row in enumerate(newgrid):
            for index_col, col in enumerate(row):
                if col == 1:
                    if newgrid[index_row][index_col - 1] == 3 or newgrid[index_row][index_col + 1] == 3:
                        if newgrid[index_row + 1][index_col] == 3 or newgrid[index_row - 1][index_col] == 3:
                            levelLost = True
                        if newgrid[index_row + 1][index_col] in (1, 5) or newgrid[index_row - 1][index_col] in (1, 5):
                            lost_cube += 1
                    if newgrid[index_row][index_col - 1] in (1, 5) or newgrid[index_row][index_col + 1] in (1, 5):
                        if newgrid[index_row + 1][index_col] in (1, 5, 3) or newgrid[index_row - 1][index_col] in (1, 5, 3):
                            lost_cube += 1
                if col == 5:
                    if newgrid[index_row][index_col - 1] == 3 or newgrid[index_row][index_col + 1] == 3:
                        if newgrid[index_row + 1][index_col] in (1, 5) or newgrid[index_row - 1][index_col] in (1, 5):
                            lost_cube += 1
                    if newgrid[index_row][index_col - 1] in (1, 5) or newgrid[index_row][index_col + 1] in (1, 5):
                        if newgrid[index_row + 1][index_col] in (1, 5, 3) or newgrid[index_row - 1][index_col] in (1, 5, 3):
                            lost_cube += 1
        if lost_cube == len(self.current_level["boxes"]):
            levelLost = True
        return levelLost

    def movementHandler(self, keys, coordinates):
        x, y = coordinates
        destination = "Invalid movement !"
        if (type(keys) == pygame.key.ScancodeWrapper):
            if keys[pygame.K_LEFT]:
                destination = [x, y - 1]
            elif keys[pygame.K_RIGHT]:
                destination = [x, y + 1]
            elif keys[pygame.K_UP]:
                destination = [x - 1, y]
            elif keys[pygame.K_DOWN]:
                destination = [x + 1, y]
        elif (type(keys) == int):
            match int_to_input[keys]:
                case "LEFT":
                    destination = [x, y - 1]
                case "RIGHT":
                    destination = [x, y + 1]
                case "UP":
                    destination = [x - 1, y]
                case "DOWN":
                    destination = [x + 1, y]
        return destination

    def calculateGrid(self, key):
        newGrid = copy.deepcopy(self.grid)
        playerCoord = self.getPlayerCoordinates()
        destination = self.movementHandler(key, playerCoord)
        if destination == "Invalid movement !":
            return None

        if self.pathIsClear(destination):
            if self.grid[playerCoord[0]][playerCoord[1]] == 4:
                newGrid[playerCoord[0]][playerCoord[1]] = 2
            else:
                newGrid[playerCoord[0]][playerCoord[1]] = 0
            if self.grid[destination[0]][destination[1]] == 2:
                newGrid[destination[0]][destination[1]] = 4
            else:
                newGrid[destination[0]][destination[1]] = 9
        elif self.boxIsHere(destination):
            boxDestination = self.movementHandler(key, destination)
            if self.pathIsClear(boxDestination):
                if self.grid[playerCoord[0]][playerCoord[1]] == 4:
                    newGrid[playerCoord[0]][playerCoord[1]] = 2
                else:
                    newGrid[playerCoord[0]][playerCoord[1]] = 0

                if self.grid[destination[0]][destination[1]] == 5:
                    newGrid[destination[0]][destination[1]] = 4
                else:
                    newGrid[destination[0]][destination[1]] = 9

                if self.grid[boxDestination[0]][boxDestination[1]] == 2:
                    newGrid[boxDestination[0]][boxDestination[1]] = 5
                else:
                    newGrid[boxDestination[0]][boxDestination[1]] = 1
        return newGrid

    def updateGrid(self, key):
        newGrid = self.calculateGrid(key)
        if newGrid is None:
            return 0, False
        reward = self.getReward(newGrid)
        if self.levelIsComplete(newGrid):
            print("level complete !")
            reward = 100
        elif self.levelIsLost(newGrid):
            print("level lost !")
            reward = -100
        hasMoved = self.grid != newGrid
        if hasMoved:
            self.grid = newGrid
            # pygame.time.delay(100)
        self.count_move += 1
        return reward, (reward == 100 or reward == -100)

    def paintGrid(self):
        for rowIndex, row in enumerate(self.grid):
            for columnIndex, column in enumerate(row):
                rectangle = pygame.Rect(columnIndex * BLOCKSIZE, rowIndex * BLOCKSIZE, BLOCKSIZE, BLOCKSIZE)
                match column:
                    case 9:
                        pygame.draw.rect(self.window, RED, rectangle)
                        pygame.draw.rect(self.window, WHITE, rectangle, width=5)
                    case 1:
                        pygame.draw.rect(self.window, BLUE, rectangle)
                        pygame.draw.rect(self.window, WHITE, rectangle, width=5)
                    case 3:
                        pygame.draw.rect(self.window, BLACK, rectangle)
                        pygame.draw.rect(self.window, WHITE, rectangle, width=5)
                    case 2:
                        pygame.draw.rect(self.window, GREEN, rectangle)
                        pygame.draw.rect(self.window, WHITE, rectangle, width=5)
                    case 0:
                        pygame.draw.rect(self.window, WHITE, rectangle)
                        pygame.draw.rect(self.window, WHITE, rectangle, width=5)
                    case 4:
                        pygame.draw.rect(self.window, YELLOW, rectangle)
                        pygame.draw.rect(self.window, WHITE, rectangle, width=5)
                    case 5:
                        pygame.draw.rect(self.window, CYAN, rectangle)
                        pygame.draw.rect(self.window, WHITE, rectangle, width=5)

                pygame.display.flip()

    def getPlayerCoords(self, newGrid):
        for xindex, row in enumerate(newGrid):
            for yindex, block in enumerate(row):
                if (block == 4) or (block == 9):
                    return (xindex, yindex)

    def getGoalCoords(self, newGrid):
        goal_coords = []
        for xindex, row in enumerate(newGrid):
            for yindex, block in enumerate(row):
                if (block == 4) or (block == 2) or (block == 5):
                    goal_coords.append((xindex, yindex))
        return goal_coords

    def computeDistPlayerBox(self, newGrid):
        box_coords = self.getBoxsCoords(newGrid)
        player_coords = self.getPlayerCoords(newGrid)
        dst = []
        for box in box_coords:
            dst.append(dist(player_coords, box))
        return dst

    def computeDistBoxGoal(self, newGrid):
        box_coords = self.getBoxsCoords(newGrid)
        goal_coords = self.getGoalCoords(newGrid)
        dst = []
        for goal in goal_coords:
            for box in box_coords:
                dst.append(dist(goal, box))
        return dst

    def boxPosPlayer(self, newGrid):
        box_coords = self.getBoxsCoords(newGrid)[0]
        player_coords = self.getPlayerCoords(newGrid)
        if player_coords[0] > box_coords[0] and player_coords[1] == box_coords[1]:
            return 0
        elif player_coords[0] < box_coords[0] and player_coords[1] == box_coords[1]:
            return 1
        elif player_coords[1] > box_coords[1] and player_coords[0] == box_coords[0]:
            return 2
        elif player_coords[1] < box_coords[1] and player_coords[0] == box_coords[0]:
            return 3
        else:
            return 4

    # Board
    def computeState(self, grid):
        state = []
        for row in grid:
            state += row
        return state

    # Distances
    def computeStateDist(self, newGrid):
        state = []
        state.append(self.boxPosPlayer(newGrid))
        state += self.computeDistPlayerBox(newGrid)
        state += self.computeDistBoxGoal(newGrid)
        return state

    def computeActions(self):
        all_movements = [0, 1, 2, 3]
        possible_movements = []
        playerCoord = self.getPlayerCoordinates()
        for move in all_movements:
            destination = self.movementHandler(move, playerCoord)
            if self.pathIsClear(destination):
                possible_movements.append(move)
            elif self.boxIsHere(destination):
                possible_movements.append(move+4)
        return possible_movements

    def futurePossibleStates(self):
        actions = self.computeActions()
        states = []
        for action in actions:
            states.append(self.computeStateDist(self.calculateGrid(action)))
        return [(action, state) for action, state in zip(actions, states)]

    def boxNearGoal(self, boxCoord):
        boxs = boxCoord
        platforms = self.current_level["goals"]
        distances = []
        for box_coords in boxs:
            for platform_coords in platforms:
                distances.append(dist(box_coords, platform_coords))
        reward = 0
        for dst in distances:
            reward += (2 - dst)*(20/self.count_move)
        return reward*0.5

    def getBoxsCoords(self, newGrid):
        list_box_coord = []
        for index_row, row in enumerate(newGrid):
            for index_col, col in enumerate(row):
                if 1 == col:
                    list_box_coord.append([index_row, index_col])
                if 5 == col:
                    list_box_coord.append([index_row, index_col])
        return list_box_coord

    def boxMovedSimple(self, newGrid):
        reward = 0
        list_old_box_coord = self.getBoxsCoords(self.grid)
        list_box_coord = self.getBoxsCoords(newGrid)
        if list_old_box_coord != list_box_coord:
            reward += 5
        return reward

    def boxMoved(self, newGrid):
        reward = 0
        list_old_box_coord = self.getBoxsCoords(self.grid)
        list_box_coord = self.getBoxsCoords(newGrid)
        if list_old_box_coord != list_box_coord:
            for plateform in self.current_level['goals']:
                for old_box_coord in list_old_box_coord:
                    for box_coord in list_box_coord:
                        if dist(old_box_coord, plateform) < dist(box_coord, plateform):
                            reward -= 5
                        elif dist(old_box_coord, plateform) > dist(box_coord, plateform):
                            reward += 5
        return reward

    def getReward(self, newGrid):
        reward = -1
        reward += self.boxMovedSimple(newGrid)
        return reward


def main():
    run = True
    game = Sokoban(['levels/microban_simple.json'])
    game.nextLevel()
    game.initGrid()

    while run:
        pygame.time.delay(10)
        game.paintGrid()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        keys = pygame.key.get_pressed()
        res = game.updateGrid(keys)
        if res[0] == -100:
            game.initGrid()
        elif res[0] == 100:
            if game.nextLevel():
                game.initGrid()
            else:
                break
        game.paintGrid()

if __name__ == "__main__":
    main()
