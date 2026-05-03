import pygame
from collections import deque
from datetime import datetime

pygame.init()

WIDTH, HEIGHT = 1000, 700
TOOLBAR_HEIGHT = 90
CANVAS_RECT = pygame.Rect(0, TOOLBAR_HEIGHT, WIDTH, HEIGHT - TOOLBAR_HEIGHT)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TSIS 2 Paint Application")

canvas = pygame.Surface((WIDTH, HEIGHT - TOOLBAR_HEIGHT))
canvas.fill("white")

font = pygame.font.SysFont("arial", 20)
small_font = pygame.font.SysFont("arial", 16)

clock = pygame.time.Clock()

current_color = (0, 0, 0)
brush_size = 5
tool = "pencil"

drawing = False
start_pos = None
last_pos = None

text_active = False
text_pos = None
text_value = ""

colors = [
    ((0, 0, 0), "Black"),
    ((255, 0, 0), "Red"),
    ((0, 150, 0), "Green"),
    ((0, 0, 255), "Blue"),
    ((255, 255, 0), "Yellow"),
    ((255, 165, 0), "Orange"),
    ((255, 255, 255), "White"),
]

tools = [
    ("pencil", "Pencil"),
    ("line", "Line"),
    ("rect", "Rect"),
    ("circle", "Circle"),
    ("square", "Square"),
    ("right_triangle", "Right Tri"),
    ("equilateral_triangle", "Eq Tri"),
    ("rhombus", "Rhombus"),
    ("eraser", "Eraser"),
    ("fill", "Fill"),
    ("text", "Text"),
]


def canvas_pos(pos):
    x, y = pos
    return x, y - TOOLBAR_HEIGHT


def is_on_canvas(pos):
    return CANVAS_RECT.collidepoint(pos)


def draw_button(rect, text, active=False):
    color = (180, 180, 180) if active else (220, 220, 220)
    pygame.draw.rect(screen, color, rect)
    pygame.draw.rect(screen, (0, 0, 0), rect, 2)
    label = small_font.render(text, True, (0, 0, 0))
    screen.blit(label, (rect.x + 5, rect.y + 8))


def draw_toolbar():
    screen.fill((200, 200, 200), (0, 0, WIDTH, TOOLBAR_HEIGHT))

    x = 10
    for tool_name, label in tools:
        rect = pygame.Rect(x, 10, 75, 30)
        draw_button(rect, label, tool == tool_name)
        x += 80

    x = 10
    for color, name in colors:
        rect = pygame.Rect(x, 50, 35, 30)
        pygame.draw.rect(screen, color, rect)
        pygame.draw.rect(screen, (0, 0, 0), rect, 2)
        if color == current_color:
            pygame.draw.rect(screen, (255, 0, 255), rect, 4)
        x += 45

    size_text = font.render(f"Brush: {brush_size}px   Press 1/2/3", True, (0, 0, 0))
    screen.blit(size_text, (360, 55))

    save_text = font.render("Ctrl+S = Save", True, (0, 0, 0))
    screen.blit(save_text, (620, 55))


def get_tool_by_click(pos):
    x = 10
    for tool_name, label in tools:
        rect = pygame.Rect(x, 10, 75, 30)
        if rect.collidepoint(pos):
            return tool_name
        x += 80
    return None


def get_color_by_click(pos):
    x = 10
    for color, name in colors:
        rect = pygame.Rect(x, 50, 35, 30)
        if rect.collidepoint(pos):
            return color
        x += 45
    return None


def draw_shape(surface, tool_name, start, end, color, width):
    x1, y1 = start
    x2, y2 = end

    if tool_name == "line":
        pygame.draw.line(surface, color, start, end, width)

    elif tool_name == "rect":
        rect = pygame.Rect(min(x1, x2), min(y1, y2), abs(x2 - x1), abs(y2 - y1))
        pygame.draw.rect(surface, color, rect, width)

    elif tool_name == "circle":
        radius = int(((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5)
        pygame.draw.circle(surface, color, start, radius, width)

    elif tool_name == "square":
        side = min(abs(x2 - x1), abs(y2 - y1))
        rect = pygame.Rect(x1, y1, side if x2 >= x1 else -side, side if y2 >= y1 else -side)
        rect.normalize()
        pygame.draw.rect(surface, color, rect, width)

    elif tool_name == "right_triangle":
        points = [(x1, y1), (x1, y2), (x2, y2)]
        pygame.draw.polygon(surface, color, points, width)

    elif tool_name == "equilateral_triangle":
        points = [(x1, y2), ((x1 + x2) // 2, y1), (x2, y2)]
        pygame.draw.polygon(surface, color, points, width)

    elif tool_name == "rhombus":
        center_x = (x1 + x2) // 2
        center_y = (y1 + y2) // 2
        points = [
            (center_x, y1),
            (x2, center_y),
            (center_x, y2),
            (x1, center_y),
        ]
        pygame.draw.polygon(surface, color, points, width)


def flood_fill(surface, start, new_color):
    width, height = surface.get_size()
    x, y = start

    if x < 0 or x >= width or y < 0 or y >= height:
        return

    old_color = surface.get_at((x, y))[:3]

    if old_color == new_color:
        return

    queue = deque()
    queue.append((x, y))

    while queue:
        x, y = queue.popleft()

        if x < 0 or x >= width or y < 0 or y >= height:
            continue

        if surface.get_at((x, y))[:3] != old_color:
            continue

        surface.set_at((x, y), new_color)

        queue.append((x + 1, y))
        queue.append((x - 1, y))
        queue.append((x, y + 1))
        queue.append((x, y - 1))


def save_canvas():
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"canvas_{timestamp}.png"
    pygame.image.save(canvas, filename)
    print(f"Saved: {filename}")


running = True

while running:
    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            keys = pygame.key.get_pressed()

            if keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL]:
                if event.key == pygame.K_s:
                    save_canvas()

            if event.key == pygame.K_1:
                brush_size = 2
            elif event.key == pygame.K_2:
                brush_size = 5
            elif event.key == pygame.K_3:
                brush_size = 10

            if text_active:
                if event.key == pygame.K_RETURN:
                    rendered_text = font.render(text_value, True, current_color)
                    canvas.blit(rendered_text, text_pos)
                    text_active = False
                    text_value = ""

                elif event.key == pygame.K_ESCAPE:
                    text_active = False
                    text_value = ""

                elif event.key == pygame.K_BACKSPACE:
                    text_value = text_value[:-1]

                else:
                    text_value += event.unicode

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                clicked_tool = get_tool_by_click(event.pos)
                clicked_color = get_color_by_click(event.pos)

                if clicked_tool:
                    tool = clicked_tool
                    text_active = False

                elif clicked_color:
                    current_color = clicked_color

                elif is_on_canvas(event.pos):
                    pos = canvas_pos(event.pos)

                    if tool == "fill":
                        flood_fill(canvas, pos, current_color)

                    elif tool == "text":
                        text_active = True
                        text_pos = pos
                        text_value = ""

                    else:
                        drawing = True
                        start_pos = pos
                        last_pos = pos

        if event.type == pygame.MOUSEMOTION:
            if drawing and is_on_canvas(event.pos):
                pos = canvas_pos(event.pos)

                if tool == "pencil":
                    pygame.draw.line(canvas, current_color, last_pos, pos, brush_size)
                    last_pos = pos

                elif tool == "eraser":
                    pygame.draw.line(canvas, (255, 255, 255), last_pos, pos, brush_size)
                    last_pos = pos

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and drawing:
                if is_on_canvas(event.pos):
                    end_pos = canvas_pos(event.pos)

                    if tool not in ["pencil", "eraser"]:
                        draw_shape(canvas, tool, start_pos, end_pos, current_color, brush_size)

                drawing = False
                start_pos = None
                last_pos = None

    screen.fill((255, 255, 255))
    draw_toolbar()
    screen.blit(canvas, (0, TOOLBAR_HEIGHT))

    if drawing and start_pos and is_on_canvas(mouse_pos):
        preview = canvas.copy()
        end_pos = canvas_pos(mouse_pos)

        if tool not in ["pencil", "eraser"]:
            draw_shape(preview, tool, start_pos, end_pos, current_color, brush_size)

        screen.blit(preview, (0, TOOLBAR_HEIGHT))

    if text_active:
        preview_text = font.render(text_value + "|", True, current_color)
        screen.blit(preview_text, (text_pos[0], text_pos[1] + TOOLBAR_HEIGHT))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()