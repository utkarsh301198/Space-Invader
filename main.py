import pygame
import os.path
import random
import math
from pygame import mixer

pygame.init()

screen = pygame.display.set_mode((800, 600))

filepath = os.path.dirname(__file__)
background = pygame.image.load(os.path.join(filepath, 'background.png'))
mixer.music.load(os.path.join(os.path.dirname(__file__), "background.wav"))
mixer.music.play(-1)

pygame.display.set_caption("Space Invader")
filepath = os.path.dirname(__file__)
icon = pygame.image.load(os.path.join(filepath, "ufo.png"))
pygame.display.set_icon(icon)

filepath = os.path.dirname(__file__)
playerImg = pygame.image.load(os.path.join(filepath, "space-invaders.png"))
playerX = 370
playerY = 480
playerX_change = 0

enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
no_of_enemies = 6

for i in range(no_of_enemies):
    filepath = os.path.dirname(__file__)
    enemyImg.append(pygame.image.load(os.path.join( filepath , "space-invader.png")))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(5)
    enemyY_change.append(40)

filepath = os.path.dirname(__file__)
bulletImg = pygame.image.load(os.path.join(filepath, "bullet.png"))
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 20
bullet_state = "ready"

score_value = 0
font = pygame.font.Font('freesansbold.ttf',32)

textX = 10
textY = 10

over_font = pygame.font.Font('freesansbold.ttf',64)

def show_score(x,y):
    score = font.render("Score:"+str(score_value),True,(255,255,255))
    screen.blit(score, (x, y))

def game_over_text():
    over_text = over_font.render("GAME OVER",True,(255,255,255))
    screen.blit(over_text, (200, 250))


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


running = True
while running:
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
           running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -8
            if event.key == pygame.K_RIGHT:
                playerX_change = 8
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound=mixer.Sound(os.path.join(os.path.dirname(__file__),'laser.wav'))
                    bullet_sound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    if playerX >= 736:
        playerX = 736

    for i in range(no_of_enemies):
        if enemyY[i]>440:
            for j in range(no_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 5
            enemyY[i] += enemyY_change[i]
        if enemyX[i] >= 736:
            enemyX_change[i] = -5
            enemyY[i] += enemyY_change[i]
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_sound = mixer.Sound(os.path.join(os.path.dirname(__file__), 'explosion.wav'))
            explosion_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value+= 1
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change




    player(playerX, playerY)
    show_score(textX,textY)
    pygame.display.update()
