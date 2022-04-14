import pygame   

pygame.init()  
window = pygame.display.set_mode((600, 600)) 
pygame.display.set_caption("Sokoban") 

run = True

class Player:
  def __init__(self):
    self.x = 200
    self.y = 200
    self.width = 40
    self.height = 40
    self.vel = 40
    self.hasMoved = False

class Game(Player):

  def __init__(self):
    super(Player, self).__init__()
    self.frame = 0
    self.wallCoordinates = []

  def init_pygame(self):
    pygame.init()
    pygame.font.init()

    
  def drawWall(self,x,y):
    self.wallCoordinates.append([x,y])
    width = 40
    height = 40
    pygame.draw.rect(window, (0, 255, 0), (x, y, width, height))  

  def noWallCollision(self, x, y):
    noCollision = True
    for wall in self.wallCoordinates :
      if wall[0] == x and wall[1] == y :
        noCollision = False
    return noCollision


game = Game()
player = Player()
game.init_pygame()

while run: 
    pygame.time.delay(20) 
    player.hasMoved = False
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: 
            run = False
    keys = pygame.key.get_pressed() 
    if keys[pygame.K_LEFT] and player.x>0 and game.noWallCollision(player.x-player.vel, player.y): 
        player.x -= player.vel
        player.hasMoved = True
    if keys[pygame.K_RIGHT] and player.x<600-player.width and game.noWallCollision(player.x+player.vel, player.y): 
        player.x += player.vel 
        player.hasMoved = True
    if keys[pygame.K_UP] and player.y>0 and game.noWallCollision(player.x, player.y-player.vel): 
        player.y -= player.vel 
        player.hasMoved = True
    if keys[pygame.K_DOWN] and player.y<600-player.height and game.noWallCollision(player.x, player.y+player.vel): 
        player.y += player.vel 
        player.hasMoved = True
    window.fill((0, 0, 0)) 
    pygame.draw.rect(window, (255, 0, 0), (player.x, player.y, player.width, player.height)) 
    game.drawWall(0,0)
    pygame.display.update()  
    if(player.hasMoved):
      pygame.time.delay(200)
pygame.quit() 

