import pygame
import random

pygame.init()

WIDTH, HEIGHT = 600, 400
CELL = 20

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mini Snake")

clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 25)

BLACK = (0, 0, 0)
GREEN = (0, 200, 80)
RED = (220, 40, 40)
WHITE = (255, 255, 255)

snake = [(300, 200)]
direction = (CELL, 0)

food = (
    random.randrange(0, WIDTH, CELL),
    random.randrange(0, HEIGHT, CELL)
)

score = 0
level = 1
speed = 8
running = True

while running:
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != (0, CELL):
                direction = (0, -CELL)
            elif event.key == pygame.K_DOWN and direction != (0, -CELL):
                direction = (0, CELL)
            elif event.key == pygame.K_LEFT and direction != (CELL, 0):
                direction = (-CELL, 0)
            elif event.key == pygame.K_RIGHT and direction != (-CELL, 0):
                direction = (CELL, 0)

    head_x, head_y = snake[0]
    new_head = (head_x + direction[0], head_y + direction[1])

    if (
        new_head[0] < 0 or new_head[0] >= WIDTH or
        new_head[1] < 0 or new_head[1] >= HEIGHT or
        new_head in snake
    ):
        running = False

    snake.insert(0, new_head)

    if new_head == food:
        score += 1

        if score % 3 == 0:
            level += 1
            speed += 2

        while True:
            food = (
                random.randrange(0, WIDTH, CELL),
                random.randrange(0, HEIGHT, CELL)
            )
            if food not in snake:
                break
    else:
        snake.pop()

    for part in snake:
        pygame.draw.rect(screen, GREEN, (*part, CELL, CELL))

    pygame.draw.rect(screen, RED, (*food, CELL, CELL))

    text = font.render(f"Score: {score}  Level: {level}", True, WHITE)
    screen.blit(text, (10, 10))

    pygame.display.update()
    clock.tick(speed)

pygame.quit()