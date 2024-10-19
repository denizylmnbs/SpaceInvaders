import pygame
import random
import math
from pygame import mixer

# Initialize the pygame
pygame.init()

# Create the screen
screen = pygame.display.set_mode((800, 600))

# Title and Icon
pygame.display.set_caption("SpaceInvaders")
icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)

# Background
background = pygame.image.load("background.jpg")

# Background Sound
mixer.music.load('background.wav')
mixer.music.play(-1)

# Player
playerImg = pygame.image.load('spaceship.png')
playerX = 370
playerY = 480
playerXChange = 0
playerYChange = 0


# score
score_value = 0  
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
textY = 10

# game over
over_font = pygame.font.Font('freesansbold.ttf', 64)
game_over = False

def game_over_text():
    over_text = font.render("GAME OVER", True, (255,255,255))
    screen.blit(over_text, (300,250))

def show_score(x,y):
    score = font.render("Score: " + str(score_value), True, (255,255,255))
    screen.blit(score, (x,y))
# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyXChange = []
numOfEnemies = 6

for i in range(numOfEnemies):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0, 800))
    enemyY.append(random.randint(50, 150))
    enemyXChange.append(random.random()/2)



# Bullet
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletXChange = 0
bulletYChange = 0.5
bulletStatus = "ready"

def player(x,y):
    screen.blit(playerImg,(x, y))
    
def enemy(x,y, i):
    screen.blit(enemyImg[i],(x,y))
    
def fire_bullet(x,y):
    global bulletStatus
    bulletStatus = "fire"
    screen.blit(bulletImg, (x+24,y-10))

def isCollision(enemyX,enemyY,BulletX,BulletY):
    distance = math.sqrt((math.pow(enemyX-bulletX, 2)) + (math.pow(enemyY-bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False
# Screen Loop
running = True
while running:
        # RGB
    screen.fill((29,43,114))
        # Background
    screen.blit(background, (0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerXChange = -0.1
            if event.key == pygame.K_RIGHT:
                playerXChange = 0.1
            if event.key == pygame.K_UP:
                playerYChange = -0.1
            if event.key == pygame.K_DOWN:
                playerYChange = 0.1                      
            if event.key == pygame.K_SPACE:
                if bulletStatus is "ready":
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()
                    bulletX = playerX
                    bulletY = playerY
                    fire_bullet(playerX, playerY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerXChange = 0
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                playerYChange = 0


        
            
    playerX += playerXChange
    playerY += playerYChange  
    
    
    
    # Bullet Movement
    if bulletY <= 0:
        bulletY = 480
        bulletStatus = "ready"
    if bulletStatus is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletYChange  
        

        
 
    
    for i in range(numOfEnemies):
        distanceToPlayer = math.sqrt((math.pow(enemyX[i]-playerX, 2) + (math.pow(enemyY[i]-playerY, 2))))
        if distanceToPlayer < 27:
            game_over = True
            for j in range(numOfEnemies):
                enemyY[j]= 2000
            break
        if game_over:
            game_over_text()
            
            
    
        if enemyX[i] <= 0:
            enemyX[i] = 0
            enemyXChange[i] *= -1
            enemyY[i] += 24
        elif enemyX[i] >= 736:
            enemyX[i] = 736
            enemyXChange[i] *= -1
            enemyY[i] += 24
           # IsCollision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion = mixer.Sound('explosion.wav')
            explosion.play()
            bulletY = 480
            bulletStatus = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 800)
            enemyY[i] = random.randint(50, 150)
        
        enemy(enemyX[i], enemyY[i], i)
        enemyX[i] += enemyXChange[i]
        
    
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736
    elif playerY <= 300:
        playerY = 300
    elif playerY >= 500:
        playerY = 500
    
    player(playerX,playerY)
    show_score(textX, textY)
    pygame.display.update()
            