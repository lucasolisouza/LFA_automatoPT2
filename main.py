import AFD
import pygame
from random import randint

pygame.init()
x = 50 #50 posição ideal; 580 máx; 0 min;
y = 300
coord_x = 700
speed = 50
speed_star = 20
window = pygame.display.set_mode((700, 480))
pygame.display.set_caption("NINJA")

background = pygame.image.load('arena.png')
ninja = pygame.image.load('01.gif')
estrela = pygame.image.load('estrela-removebg-preview.png')
nave = pygame.image.load('fly.png')

# Music
pygame.mixer.music.load('awesomeness.wav')
pygame.mixer.music.play(-1)

# text of gameover
font = pygame.font.SysFont('arial black',30)
text = font.render("GAME OVER!",True,(255,255,255),(0,0,0))
pos_text = text.get_rect()
pos_text.center = (100,100)


window_open = True
while window_open:
    i = 0
    pygame.time.delay(50)
    for event in pygame.event.get():
        commands = pygame.key.get_pressed()
        if event.type == pygame.QUIT:
            window_open = False
    if commands[pygame.K_UP] and y >= 50:
        i = 1
        y -= speed
    if commands[pygame.K_DOWN] and y <= 280:
        y += speed
    if commands[pygame.K_RIGHT] and x <= 500:
        x += speed
    if commands[pygame.K_LEFT] and x >= 50:
        x -= speed
    f = 0
    #colisão
    if (x + 50 > coord_x - 50 and y + 50 > 320) and (x - 50 < coord_x - 50 and y + 50 > 320):
        pygame.mixer.music.stop()
        y = 1200

    coord_x -= speed_star
    if coord_x < 0:
        coord_x = randint(700,2000)

    window.blit(background, (0,0))
    if i == 1:
        window.blit(nave, (x, y))
    else:
        window.blit(ninja, (x, y))
    #window.blit(ninja, (x, y))
    window.blit(estrela, (coord_x,320))

    pygame.display.update()

pygame.quit()
