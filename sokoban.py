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

    def __init__(self, list_level) -> None:
        self.list_level = list_level

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
        for index_row, row in enumerate(newgrid):
            if 1 in row:
                index_col = row.index(1)
                if newgrid[index_row][index_col - 1] in (3, 5) or newgrid[index_row][index_col + 1] in (3, 5):
                    if newgrid[index_row + 1][index_col] in (3, 5) or newgrid[index_row - 1][index_col] in (3, 5):
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
        newGrid = self.grid
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
        reward = self.getReward()
        if self.levelIsComplete(newGrid):
            # print("level complete !")
            reward = 11
        elif self.levelIsLost(newGrid):
            # print("level lost !")
            reward = -11
        hasMoved = self.grid == newGrid
        if hasMoved:
            self.grid = newGrid
            pygame.time.delay(100)
        return reward, (reward==11 or reward==-11)

    def paintGrid(self):
        for rowIndex, row in enumerate(self.grid):
            for columnIndex, column in enumerate(row):
                rectangle = pygame.Rect(columnIndex * BLOCKSIZE, rowIndex * BLOCKSIZE, BLOCKSIZE, BLOCKSIZE)
                match column:
                    case 9:
                        pygame.draw.rect(window, RED, rectangle)
                        pygame.draw.rect(window, WHITE, rectangle, width=5)
                    case 1:
                        pygame.draw.rect(window, BLUE, rectangle)
                        pygame.draw.rect(window, WHITE, rectangle, width=5)
                    case 3:
                        pygame.draw.rect(window, BLACK, rectangle)
                        pygame.draw.rect(window, WHITE, rectangle, width=5)
                    case 2:
                        pygame.draw.rect(window, GREEN, rectangle)
                        pygame.draw.rect(window, WHITE, rectangle, width=5)
                    case 0:
                        pygame.draw.rect(window, WHITE, rectangle)
                        pygame.draw.rect(window, WHITE, rectangle, width=5)
                    case 4:
                        pygame.draw.rect(window, YELLOW, rectangle)
                        pygame.draw.rect(window, WHITE, rectangle, width=5)
                    case 5:
                        pygame.draw.rect(window, CYAN, rectangle)
                        pygame.draw.rect(window, WHITE, rectangle, width=5)

                pygame.display.flip()

    def computeState(self, grid):
        state = []
        for row in self.grid:
            state += row
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
        start_state = self.computeState(self.grid)
        states = []
        for action in actions:
            states.append(self.computeState(self.calculateGrid(action)))
        return [(action, state) for action, state in zip(actions, states)]

    def getReward(self):
        init_goals = len(self.current_level['goals'])
        levelComplete = 0
        left_goals = 0
        for row in self.grid:
            if 2 in row:
                left_goals += 1
        return 1 + (init_goals - left_goals)*3


def main(level):
    run = True
    game = Sokoban(['levels/microban_0.json', 'levels/microban_1.json'])
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
        if res == -11:
            game.initGrid()
        elif res == 11:
            if game.nextLevel():
                game.initGrid()
            else:
                break
        game.paintGrid()


if __name__ == "__main__":
    main(lvl0)
