import pygame
import random
import math
from pygame import mixer

pygame.init()

# Creating game window
game_screen = pygame.display.set_mode((800, 600))
#background music
mixer.music.load("background.wav")
mixer.music.play(-1)
# Adding background
background = pygame.image.load("background.png")

# Creating caption and adding icon
pygame.display.set_caption("SPACE INVADER")
icon = pygame.image.load("ufo.png")
pygame.display.set_icon(icon)

# Player
playerimg = pygame.image.load("player.png")
playerX = 371
playerY = 480
player_xchange = 0

# Enemy
enemy_img = []
enemyX = []
enemyY = []
enemy_xchange = []
enemy_ychange = []
no_of_enemies = 6
for i in range(no_of_enemies):
    enemy_img.append(pygame.image.load("enemy.png"))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemy_xchange.append(4)
    enemy_ychange.append(50)

# Bullet
bullet_img = pygame.image.load("bullet.png")
bulletX = 0
bulletY = 480
bullet_ychange = 10
bullet_state = "ready"

score = 0

font = pygame.font.Font(None, 36)
game_over_font = pygame.font.Font(None, 64)

def player(x, y):
    game_screen.blit(playerimg, (x, y))

def enemy(x, y, index):
    game_screen.blit(enemy_img[index], (x, y))
    
def game_over_text():
    game_over_text = game_over_font.render("GAME OVER", True, (255, 0, 0))
    game_screen.blit(game_over_text, (250, 200))

def bullet_fire(x, y):
    global bullet_state, bulletX, bulletY
    if bullet_state == "ready":
        bullet_state = "fire"
        game_screen.blit(bullet_img, (x + 16, y + 10))
        bulletX = x
        bulletY = y

def iscollision(enemyX, enemyY, bulletX, bulletY):
    dis = math.sqrt((enemyX - bulletX) ** 2 + (enemyY - bulletY) ** 2)
    if dis < 27:
        return True
    else:
        return False

# Game variables
running = True

# Game loop
while running:
    game_screen.fill((0, 0, 0))
    # Adding background image
    game_screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Handle player movement and bullet firing
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_xchange = -5
            elif event.key == pygame.K_RIGHT:
                player_xchange = 5
            elif event.key == pygame.K_SPACE:
                bulletsound = mixer.Sound("laser.wav")
                bulletsound.play()
                bullet_fire(playerX, bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player_xchange = 0

    # Update player position
    playerX += player_xchange

    # Checking for boundary for the player
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Update multiple enemies
    game_over = False  # Initialize game_over to False

    for i in range(no_of_enemies):
        if enemyY[i] > 440:
            game_over = True  # If any enemy crosses y-axis of 200, set game_over to True

    if game_over:
        game_over_text()
    else:
        for i in range(no_of_enemies):
            enemyX[i] += enemy_xchange[i]

            # Check for enemy boundary and reverse direction
            if enemyX[i] <= 0:
                enemy_xchange[i] = 4
                enemyY[i] += enemy_ychange[i]
            elif enemyX[i] >= 736:
                enemy_xchange[i] = -4
                enemyY[i] += enemy_ychange[i]

            # Check for collision with each enemy
            collision = iscollision(enemyX[i], enemyY[i], bulletX, bulletY)
            if collision:
                collisionsound = mixer.Sound("explosion.wav")
                collisionsound.play()
                bulletY = 480
                bullet_state = "ready" 
                score += 1
                print(f" The score is {score}")
                enemyX[i] = random.randint(0, 800)
                enemyY[i] = random.randint(50, 150)

            # Draw each enemy
            enemy(enemyX[i], enemyY[i], i)

    # Update Bullet Movement
    if bullet_state == "fire":
        bulletY -= bullet_ychange
        if bulletY <= 0:
            bulletY = 480  # Reset the bullet position
            bullet_state = "ready"

    if bullet_state == "fire":
        game_screen.blit(bullet_img, (bulletX + 16, bulletY + 10))

    # Render and display the score
    score_text = font.render("Score: " + str(score), True, (255, 255, 255))
    game_screen.blit(score_text, (10, 10))

    # Draw player and the bullet
    player(playerX, playerY)

    pygame.display.update()
