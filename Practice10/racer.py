import pygame
import random

pygame.init()

WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mini Racer")

clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 28)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (220, 40, 40)
BLUE = (40, 100, 220)
YELLOW = (255, 220, 0)
GRAY = (80, 80, 80)

player = pygame.Rect(180, 500, 40, 70)
enemy = pygame.Rect(random.randint(50, 310), -100, 40, 70)
coin = pygame.Rect(random.randint(50, 330), -200, 25, 25)

speed = 5
coins = 0
running = True

while running:
    screen.fill(GRAY)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] and player.left > 40:
        player.x -= 6

    if keys[pygame.K_RIGHT] and player.right < WIDTH - 40:
        player.x += 6

    enemy.y += speed
    coin.y += speed

    if enemy.top > HEIGHT:
        enemy.y = -100
        enemy.x = random.randint(50, 310)
        speed += 0.2

    if coin.top > HEIGHT:
        coin.y = -200
        coin.x = random.randint(50, 330)

    if player.colliderect(coin):
        coins += 1
        coin.y = -200
        coin.x = random.randint(50, 330)

    if player.colliderect(enemy):
        running = False

    pygame.draw.rect(screen, BLACK, (30, 0, 340, HEIGHT))
    pygame.draw.rect(screen, BLUE, player)
    pygame.draw.rect(screen, RED, enemy)
    pygame.draw.ellipse(screen, YELLOW, coin)

    text = font.render(f"Coins: {coins}", True, WHITE)
    screen.blit(text, (250, 20))

    pygame.display.update()
    clock.tick(60)

pygame.quit()