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
goal + box = $


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
            self.grid[x][y] = "#"
        for x, y in self.current_level["boxes"]:
            self.grid[x][y] = "@"
        for x, y in self.current_level["goals"]:
            if self.grid[x][y] == "@":
                self.grid[x][y] = "$"
            else:
                self.grid[x][y] = "*"
        player_x, player_y = self.current_level["player"]
        self.grid[player_x][player_y] = "x"

    def getPlayerCoordinates(self):
        player_pos = [(index, row.index("x")) for index, row in enumerate(self.grid) if 'x' in row]
        if player_pos == []:
            player_pos = [(index, row.index(".")) for index, row in enumerate(self.grid) if '.' in row][0]
        else:
            player_pos = player_pos[0]
        return player_pos

    def pathIsClear(self, destination):
        x, y = destination
        return self.grid[x][y] == 0 or self.grid[x][y] == "*"

    def boxIsHere(self, destination):
        x, y = destination
        return self.grid[x][y] in ("@", "$")

    def levelIsComplete(self, newgrid):
        levelComplete = True
        for row in newgrid:
            if "*" in row:
                levelComplete = False
            elif "." in row:
                levelComplete = False
        return levelComplete

    def levelIsLost(self, newgrid):
        levelLost = False
        for index_row, row in enumerate(newgrid):
            if "@" in row:
                index_col = row.index("@")
                if newgrid[index_row][index_col - 1] in ("#", "$") or newgrid[index_row][index_col + 1] in ("#", "$"):
                    if newgrid[index_row + 1][index_col] in ("#", "$") or newgrid[index_row - 1][index_col] in ("#", "$"):
                        levelLost = True
        return levelLost

    def movementHandler(self, keys, coordinates):
        x, y = coordinates
        destination = "Invalid movement !"
        if keys[pygame.K_LEFT]:
            destination = [x, y - 1]
        elif keys[pygame.K_RIGHT]:
            destination = [x, y + 1]
        elif keys[pygame.K_UP]:
            destination = [x - 1, y]
        elif keys[pygame.K_DOWN]:
            destination = [x + 1, y]
        return destination

    def updateGrid(self, keys):
        newGrid = self.grid
        playerCoord = self.getPlayerCoordinates()
        destination = self.movementHandler(keys, playerCoord)
        if destination == "Invalid movement !":
            return

        if self.pathIsClear(destination):
            if self.grid[playerCoord[0]][playerCoord[1]] == ".":
                newGrid[playerCoord[0]][playerCoord[1]] = "*"
            else:
                newGrid[playerCoord[0]][playerCoord[1]] = 0
            if self.grid[destination[0]][destination[1]] == "*":
                newGrid[destination[0]][destination[1]] = "."
            else:
                newGrid[destination[0]][destination[1]] = "x"
        elif self.boxIsHere(destination):
            boxDestination = self.movementHandler(keys, destination)
            if self.pathIsClear(boxDestination):
                if self.grid[playerCoord[0]][playerCoord[1]] == ".":
                    newGrid[playerCoord[0]][playerCoord[1]] = "*"
                else:
                    newGrid[playerCoord[0]][playerCoord[1]] = 0

                if self.grid[destination[0]][destination[1]] == "$":
                    newGrid[destination[0]][destination[1]] = "."
                else:
                    newGrid[destination[0]][destination[1]] = "x"

                if self.grid[boxDestination[0]][boxDestination[1]] == "*":
                    newGrid[boxDestination[0]][boxDestination[1]] = "$"
                else:
                    newGrid[boxDestination[0]][boxDestination[1]] = "@"
        reward = self.getReward()
        if self.levelIsComplete(newGrid):
            print("level complete !")
            reward = 10
        elif self.levelIsLost(newGrid):
            print("level lost !")
            reward = -10
        hasMoved = self.grid == newGrid
        if hasMoved:
            self.grid = newGrid
            pygame.time.delay(100)
        return reward

    def paintGrid(self):
        for rowIndex, row in enumerate(self.grid):
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
                        pygame.draw.rect(window, YELLOW, rectangle)
                        pygame.draw.rect(window, WHITE, rectangle, width=5)
                    case "$":
                        pygame.draw.rect(window, CYAN, rectangle)
                        pygame.draw.rect(window, WHITE, rectangle, width=5)

                pygame.display.flip()

    def simulateStep(self, key):
        match key:
            case "LEFT":
                self.grid = self.updateGrid("LEFT")
            case "DOWN":
                self.grid = self.updateGrid("DOWN")
            case "RIGHT":
                self.grid = self.updateGrid("RIGHT")
            case "UP":
                self.grid = self.updateGrid("UP")

    def computeState(self):
        state = []
        for row in self.grid:
            state += row
        return state

    def computeActions(self):
        all_movements = ["LEFT", "DOWN", "RIGHT", "UP"]
        possible_movements = []
        playerCoord = self.getPlayerCoordinates()
        for index, move in enumerate(all_movements):
            destination = self.movementHandler(move, playerCoord)
            if self.pathIsClear(destination):
                possible_movements.append(index)
            elif self.boxIsHere(destination):
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

    def futurePossibleStates(self):
        actions = self.computeActions()
        start_state = self.computeState()
        states = []
        for action in actions:
            states.append(self.computeState(self.simulateStep(action)))
        return [(action, state) for action, state in zip(actions, states)]

    def getReward(self):
        init_goals = len(self.current_level['goals'])
        levelComplete = 0
        left_goals = 0
        for row in self.grid:
            if "*" in row:
                left_goals += 1
        if left_goals == 0:
            levelComplete = 1
        return 1 + levelComplete*10 + (init_goals - left_goals)*5


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
        if res == -10:
            game.initGrid()
        elif res == 10:
            if game.nextLevel():
                game.initGrid()
            else:
                break
        game.paintGrid()


if __name__ == "__main__":
    main(lvl0)
