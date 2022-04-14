import pygame   

pygame.init()  
window = pygame.display.set_mode((600, 600)) 
pygame.display.set_caption("Sokoban") 
x = 200
y = 200
width = 40
height = 40
vel = 40
run = True
while run: 
    pygame.time.delay(100) 
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: 
            run = False
    keys = pygame.key.get_pressed() 
    if keys[pygame.K_LEFT] and x>0: 
        x -= vel 
    if keys[pygame.K_RIGHT] and x<600-width: 
        x += vel 
    if keys[pygame.K_UP] and y>0: 
        y -= vel 
    if keys[pygame.K_DOWN] and y<600-height: 
        y += vel 
    window.fill((0, 0, 0)) 
    pygame.draw.rect(window, (255, 0, 0), (x, y, width, height)) 
    pygame.display.update()  
pygame.quit() 