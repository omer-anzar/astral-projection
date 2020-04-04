import pygame
import random
import math
from pygame import mixer

# Intialize the pygame
pygame.init()

# screen height = 600 and width = 800
screen = pygame.display.set_mode((800, 600))
# in pygame (0,0) is on left top.
# left to right x increases
# top to bottom y increases

# Background
background = pygame.image.load("background.png")

# Back Music
mixer.music.load('STAY.mp3')
mixer.music.play(-1) # this will play the music on loop

# Title and Icon
pygame.display.set_caption("Space Invaders created by paradox_omer")
icon = pygame.image.load('spaceship.png')
pygame.display.set_icon (icon)

# Player
playerImg = pygame.image.load('character.png')
playerX = 370
playerY = 480
playerX_change = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 10

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('ufo.png'))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(8)
    enemyY_change.append(40)

# Bullet
#   Ready - State meants you cant see the bullet on the screen
#   Fire - The bullet is currently moving
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480 # same position where space ship is located
bulletX_change = 0
bulletY_change = 20
bullet_state = "ready"

# Score
score_value = 0
loss_value = 0
font = pygame.font.Font('freesansbold.ttf', 25)
textX = 10
textY = 10
lossX = 670
lossY = 10
borderline = pygame.font.Font('freesansbold.ttf', 10)
borderlineX = 0
borderlineY = 430

# Game over text
over_font = pygame.font.Font('freesansbold.ttf', 60)

# Functions

def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

def show_loss(x, y):
    loss = font.render("Loss: " + str(loss_value)+" \ 3", True, (255, 255, 255))
    screen.blit(loss, (x, y))

def game_over_text():
    over_text = over_font.render("Score:"+ str(score_value)+" GAME OVER" , True, (255, 255, 255))
    screen.blit(over_text, (100, 250))

def show_borderline(x, y):
    border = borderline.render("_"*800, True, (0, 255, 0))
    screen.blit(border, (x, y))

def player(x, y):
    screen.blit(playerImg, (x, y)) #means to draw. it draws image on screen

def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))#16 x axis will placed bullet on mid of spaceship and 10 y axis will placed it a little bit above spaceship

def isCollision (enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(((enemyX - bulletX)**2) + ((enemyY - bulletY)**2))
    if distance < 35:
        return True
    else:
        return False

def isCollisionWithSpaceship(enemyY):
    if enemyY >= 410:
        return True
    else:
        return False
    
# Game Loop
running = True
while running:
    # RGB Red, Green, Blue (search google for code)
    #screen.fill((0, 0, 0))  #255 is max color opacity
    
    # Background image
    screen.blit(background, (0,0))
    for event in pygame.event.get(): #any type of control happens in event
        if event.type == pygame.QUIT: # close button
            running = False
    
        # if keystroke is pressed check wheter its right or left
        if event.type == pygame.KEYDOWN: # keydown = pressing key
            if event.key == pygame.K_LEFT:
                playerX_change = -7               
            if event.key == pygame.K_RIGHT:
                playerX_change = 7                
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bullet_Sound = mixer.Sound('laser.wav')
                    bullet_Sound.set_volume(0.2)# volume b/w 0-1
                    bullet_Sound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
        if event.type == pygame.KEYUP: # keyup = key release 
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
                
        

    # always put player img after screenfill because screen is drawn first
    #then character is draw on the screen not behind
    playerX += playerX_change
    
    # Borders
    if playerX <= 0:
        playerX = 0
    elif playerX >=736:
        playerX = 736
    
    #   enemey movements
    for i in range(num_of_enemies):
        # Game over
        if loss_value > 3:
            for j in range(num_of_enemies):
                enemyX[i] = 2000 # send them out of the screen
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]

        if enemyX[i] <= 0:
            enemyX_change[i] *= -1
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >=736:
            enemyX_change[i] *= -1
            enemyY[i] += enemyY_change[i]
    
        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_Sound = mixer.Sound('explosion.wav')
            explosion_Sound.set_volume(0.2)# volume b/w 0-1
            explosion_Sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            print('score', score_value)
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)
        
        # Colision with spaceship
        collision = isCollisionWithSpaceship(enemyY[i])
        if collision:
            loss_value += 1
            print("Loss", loss_value)
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    # Bullet movement
    if bulletY <= -10:
        bulletY = 400
        bullet_state = "ready"
    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change


    show_borderline(borderlineX, borderlineY)
    player(playerX, playerY)
    show_score(textX, textY)
    show_loss(lossX, lossY)
    pygame.display.update() #update the display every time (pixel by pixel)
