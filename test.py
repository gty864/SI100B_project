import pygame
import sys

width, height = 800, 600
win = pygame.display.set_mode((width,height))

#load game asserts
bg = pygame.image.load("grass.png")
player = pygame.image.load("player.png")
player = pygame.transform.scale(player,(50,50))
player_rect = player.get_rect()
player_rect.center = (width//2, height//2)

speed = 8

clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player_rect.y -= speed
    if keys[pygame.K_s]:
        player_rect.y += speed
    if keys[pygame.K_d]:
        player_rect.x += speed
    if keys[pygame.K_a]:
        player_rect.x -= speed  
    

    pygame.display.flip()
    win.blit(bg, (0,0))
    win.blit(player,player_rect)
    clock.tick(30)

