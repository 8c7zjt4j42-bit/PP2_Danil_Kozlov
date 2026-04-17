import pygame
import math
import datetime
import os


WIDTH = 800
HEIGHT = 800
CENTER = (WIDTH // 2, HEIGHT // 2)


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)


def draw_hand(screen, angle_degrees, length, color, thickness):
    
    angle_radians = math.radians(angle_degrees - 90)

    
    end_x = CENTER[0] + length * math.cos(angle_radians)
    end_y = CENTER[1] + length * math.sin(angle_radians)

    
    pygame.draw.line(screen, color, CENTER, (end_x, end_y), thickness)


def run_clock():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Mickey Clock")

    clock = pygame.time.Clock()

    
    current_dir = os.path.dirname(__file__)
    image_path = os.path.join(current_dir, "images", "mickeyclock.jpeg")

    
    background = pygame.image.load(image_path)
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        
        now = datetime.datetime.now()
        minutes = now.minute
        seconds = now.second

        
        minute_angle = (minutes / 60) * 360
        second_angle = (seconds / 60) * 360

        
        screen.fill(WHITE)
        screen.blit(background, (0, 0))

        
        draw_hand(screen, minute_angle, 220, BLACK, 8)

        
        draw_hand(screen, second_angle, 220, RED, 4)

        
        pygame.draw.circle(screen, BLACK, CENTER, 7)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()