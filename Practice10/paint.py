import pygame

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mini Paint")

clock = pygame.time.Clock()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (220, 40, 40)
GREEN = (0, 200, 80)
BLUE = (40, 100, 220)

screen.fill(WHITE)

color = BLACK
tool = "circle"
drawing = False
start_pos = None
radius = 8

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                color = BLACK
            elif event.key == pygame.K_2:
                color = RED
            elif event.key == pygame.K_3:
                color = GREEN
            elif event.key == pygame.K_4:
                color = BLUE
            elif event.key == pygame.K_e:
                color = WHITE
            elif event.key == pygame.K_c:
                tool = "circle"
            elif event.key == pygame.K_r:
                tool = "rect"
            elif event.key == pygame.K_BACKSPACE:
                screen.fill(WHITE)

        if event.type == pygame.MOUSEBUTTONDOWN:
            drawing = True
            start_pos = event.pos

        if event.type == pygame.MOUSEBUTTONUP:
            drawing = False
            end_pos = event.pos

            if tool == "rect":
                x1, y1 = start_pos
                x2, y2 = end_pos
                rect = pygame.Rect(
                    min(x1, x2),
                    min(y1, y2),
                    abs(x2 - x1),
                    abs(y2 - y1)
                )
                pygame.draw.rect(screen, color, rect, 3)

            elif tool == "circle":
                x1, y1 = start_pos
                x2, y2 = end_pos
                r = int(((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5)
                pygame.draw.circle(screen, color, start_pos, r, 3)

    if drawing and pygame.mouse.get_pressed()[0] and tool == "brush":
        pygame.draw.circle(screen, color, pygame.mouse.get_pos(), radius)

    keys = pygame.key.get_pressed()

    if keys[pygame.K_b]:
        tool = "brush"

    pygame.display.update()
    clock.tick(60)

pygame.quit()