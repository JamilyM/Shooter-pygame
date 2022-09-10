import pygame
import random

pygame.init()

x = 1280
y = 720

screen = pygame.display.set_mode((x, y))
pygame.display.set_caption('Meu jogo em Python')

font = pygame.font.SysFont('font/PixelGameFont.ttf', 50)

bg = pygame.image.load('images/bg.jpg').convert_alpha()
bg = pygame.transform.scale(bg, (x, y))

alien = pygame.image.load('images/spaceship.png').convert_alpha()
alien = pygame.transform.scale(alien, (50, 50))

playerImg = pygame.image.load('images/space.png').convert_alpha()
playerImg = pygame.transform.scale(
    playerImg, (50, 50))  # conversão do tamanho da nave
playerImg = pygame.transform.rotate(playerImg, -90)

missil = pygame.image.load('images/missile.png').convert_alpha()
missil = pygame.transform.scale(missil, (25, 25))
missil = pygame.transform.rotate(missil, -45)

pos_alien_x = 500
pos_alien_y = 360

pos_player_x = 200
pos_player_y = 300

vel_missil_x = 0
pos_missil_x = 200
pos_missil_y = 300

pontos = 3

triggered = False
rodando = True

player_rect = playerImg.get_rect()
alien_rect = alien.get_rect()
missil_rect = missil.get_rect()

# funções para que o alien se movimente aleatoriamente


def respawn():
    x = 1350
    y = random.randint(1, 640)
    return [x, y]


def respawn_missil():
    triggered = False
    respawn_missil_x = pos_player_x
    respawn_missil_y = pos_player_y
    vel_missil_x = 0
    return [respawn_missil_x, respawn_missil_y, triggered, vel_missil_x]


def colisions():
    global pontos
    if player_rect.colliderect(alien_rect) or alien_rect.x == 60:
        pontos -= 1
        return True
    elif missil_rect.colliderect(alien_rect):
        pontos += 1
        return True
    else:
        return False


while rodando:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False

    screen.blit(bg, (0, 0))

    rel_x = x % bg.get_rect().width
    # criar background dentro da execução
    screen.blit(bg, (rel_x - bg.get_rect().width, 0))
    if rel_x < 1280:
        screen.blit(bg, (rel_x, 0))

    # teclas
    tecla = pygame.key.get_pressed()
    if tecla[pygame.K_UP] and pos_player_y > 1:
        pos_player_y -= 1
        if not triggered:
            pos_missil_y -= 1

    if tecla[pygame.K_DOWN] and pos_player_y < 665:
        pos_player_y += 1

        if not triggered:
            pos_missil_y += 1

    if tecla[pygame.K_SPACE]:
        triggered = True
        if pontos > 5 and 10 >= pontos:
            vel_missil_x = 2.5
        elif pontos > 10:
            vel_missil_x = 3.5
        else:
            vel_missil_x = 2

    if pontos == 0:
        rodando = False

    # respawn
    if pos_alien_x == 50:
        pos_alien_x = respawn()[0]
        pos_alien_y = respawn()[1]

    if pos_missil_x == 1300:
        pos_missil_x, pos_missil_y, triggered, vel_missil_x = respawn_missil()

    if pos_alien_x == 50 or colisions():
        pos_alien_x = respawn()[0]
        pos_alien_y = respawn()[1]

    # posição rect
    player_rect.x = pos_player_x
    player_rect.y = pos_player_y

    missil_rect.x = pos_missil_x
    missil_rect.y = pos_missil_y

    alien_rect.x = pos_alien_x
    alien_rect.y = pos_alien_y

    # movimento

    if pontos > 5 and 10 >= pontos:
        pos_alien_x -= 2
        x -= 3
    elif pontos > 10:
        pos_alien_x -= 3
        x -= 4
    else:
        pos_alien_x -= 1
        x -= 2

    # movimento do missil, depois space ele entrar em movimento já que seu valor vira 1
    pos_missil_x += vel_missil_x

    score = font.render(f' Pontos: {int(pontos)} ', True, (0, 0, 0))
    screen.blit(score, (50, 50))

    # criar as imagens dentro da execução
    screen.blit(alien, (pos_alien_x, pos_alien_y))
    screen.blit(missil, (pos_missil_x, pos_missil_y))
    screen.blit(playerImg, (pos_player_x, pos_player_y))

    pygame.display.update()
