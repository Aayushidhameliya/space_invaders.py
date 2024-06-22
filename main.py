import math
import random
import pygame
import requests
from io import BytesIO

# Initialize pygame
pygame.init()

# Set up the screen
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Background
background_url = 'https://www.techwithtim.net/wp-content/uploads/2019/08/space-invaders-background.png'
response = requests.get(background_url)
background = pygame.image.load(BytesIO(response.content)).convert()

# Sound
pygame.mixer.music.load("https://www.techwithtim.net/wp-content/uploads/2019/08/background.wav")
pygame.mixer.music.play(-1)

# Caption and Icon
pygame.display.set_caption("Space Invader")
icon_url = 'https://www.techwithtim.net/wp-content/uploads/2019/08/ufo.png'
icon_response = requests.get(icon_url)
icon = pygame.image.load(BytesIO(icon_response.content))
pygame.display.set_icon(icon)

# Player
player_url = 'https://www.techwithtim.net/wp-content/uploads/2019/08/player.png'
player_response = requests.get(player_url)
playerImg = pygame.image.load(BytesIO(player_response.content))
player_width, player_height = 64, 64
playerX = screen_width // 2 - player_width // 2
playerY = screen_height - player_height - 20
playerX_change = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemy_url = 'https://www.techwithtim.net/wp-content/uploads/2019/08/enemy.png'
    enemy_response = requests.get(enemy_url)
    enemyImg.append(pygame.image.load(BytesIO(enemy_response.content)))
    enemy_width, enemy_height = 64, 64
    enemyX.append(random.randint(0, screen_width - enemy_width))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(4)
    enemyY_change.append(40)

# Bullet
bullet_url = 'https://www.techwithtim.net/wp-content/uploads/2019/08/bullet.png'
bullet_response = requests.get(bullet_url)
bulletImg = pygame.image.load(BytesIO(bullet_response.content))
bullet_width, bullet_height = 32, 32
bulletX = 0
bulletY = 380
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX, textY = 10, 10

# Game Over
over_font = pygame.font.Font('freesansbold.ttf', 64)

def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
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
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False

# Game Loop
running = True
while running:

    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Check for keystrokes
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bulletSound = pygame.mixer.Sound("https://www.techwithtim.net/wp-content/uploads/2019/08/laser.wav")
                    bulletSound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # Move player spaceship
    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Move enemies
    for i in range(num_of_enemies):
        # Game Over
        if enemyY[i] > 380:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 4
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -4
            enemyY[i] += enemyY_change[i]

        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosionSound = pygame.mixer.Sound("https://www.techwithtim.net/wp-content/uploads/2019/08/explosion.wav")
            explosionSound.play()
            bulletY = 380
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    # Bullet Movement
    if bulletY <= 0:
        bulletY = 380
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(textX, textY)

    pygame.display.update()

# Quit pygame
pygame.quit()

