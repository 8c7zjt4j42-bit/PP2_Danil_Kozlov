import pygame

WIDTH = 500
HEIGHT = 700

WHITE = (255, 255, 255)
BLACK = (20, 20, 20)
GRAY = (100, 100, 100)
LIGHT_GRAY = (180, 180, 180)
GREEN = (0, 200, 100)
RED = (220, 50, 50)
YELLOW = (240, 210, 70)


class Button:
    def __init__(self, x, y, w, h, text):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text

    def draw(self, screen, font):
        mouse = pygame.mouse.get_pos()

        color = LIGHT_GRAY if self.rect.collidepoint(mouse) else GRAY

        pygame.draw.rect(screen, color, self.rect, border_radius=10)
        pygame.draw.rect(screen, WHITE, self.rect, 2, border_radius=10)

        text = font.render(self.text, True, WHITE)
        text_rect = text.get_rect(center=self.rect.center)
        screen.blit(text, text_rect)

    def clicked(self, event):
        return (
            event.type == pygame.MOUSEBUTTONDOWN
            and event.button == 1
            and self.rect.collidepoint(event.pos)
        )


def draw_text(screen, text, font, color, x, y, center=True):
    render = font.render(str(text), True, color)
    rect = render.get_rect()

    if center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)

    screen.blit(render, rect)


def draw_panel(screen, rect):
    pygame.draw.rect(screen, (30, 30, 30), rect, border_radius=12)
    pygame.draw.rect(screen, WHITE, rect, 2, border_radius=12)