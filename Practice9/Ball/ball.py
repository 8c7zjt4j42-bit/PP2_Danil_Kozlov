import pygame


WIDTH = 800
HEIGHT = 600


WHITE = (255, 255, 255)
RED = (255, 0, 0)


BALL_RADIUS = 25
STEP = 20


def run_game():
    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Moving Ball")

    clock = pygame.time.Clock()

    
    x = WIDTH // 2
    y = HEIGHT // 2

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if x - STEP - BALL_RADIUS >= 0:
                        x -= STEP

                elif event.key == pygame.K_RIGHT:
                    if x + STEP + BALL_RADIUS <= WIDTH:
                        x += STEP

                elif event.key == pygame.K_UP:
                    if y - STEP - BALL_RADIUS >= 0:
                        y -= STEP

                elif event.key == pygame.K_DOWN:
                    if y + STEP + BALL_RADIUS <= HEIGHT:
                        y += STEP

        screen.fill(WHITE)
        pygame.draw.circle(screen, RED, (x, y), BALL_RADIUS)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()