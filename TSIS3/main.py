import pygame

from racer import Game, CAR_COLORS, DIFFICULTIES
from persistence import load_settings, save_settings, load_leaderboard, add_score
from ui import WIDTH, HEIGHT, WHITE, GRAY, GREEN, RED, YELLOW, Button, draw_text, draw_panel


pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TSIS 3 Racer Game")
clock = pygame.time.Clock()

font = pygame.font.SysFont(None, 30)
small_font = pygame.font.SysFont(None, 24)
big_font = pygame.font.SysFont(None, 48)

settings = load_settings()

state = "menu"
game = None

player_name = ""
name_active = False
score_saved = False


def new_game():
    global game, state, score_saved
    game = Game(settings)
    score_saved = False
    state = "playing"


def draw_menu():
    screen.fill((25, 25, 25))
    draw_text(screen, "TSIS 3 RACER GAME", big_font, WHITE, WIDTH // 2, 100)

    buttons = [
        Button(150, 190, 200, 55, "Play"),
        Button(150, 260, 200, 55, "Leaderboard"),
        Button(150, 330, 200, 55, "Settings"),
        Button(150, 400, 200, 55, "Quit"),
    ]

    for button in buttons:
        button.draw(screen, font)

    draw_text(screen, "Use arrows while playing", small_font, WHITE, WIDTH // 2, 520)
    return buttons


def draw_name_screen():
    global name_active

    screen.fill((25, 25, 25))
    draw_text(screen, "Enter username", big_font, WHITE, WIDTH // 2, 120)

    box = pygame.Rect(100, 240, 300, 55)
    pygame.draw.rect(screen, (40, 40, 40), box, border_radius=8)
    pygame.draw.rect(screen, GREEN if name_active else WHITE, box, 2, border_radius=8)

    shown_name = player_name if player_name else "type here..."
    color = WHITE if player_name else GRAY
    draw_text(screen, shown_name, font, color, WIDTH // 2, 268)

    start = Button(150, 340, 200, 55, "Start")
    back = Button(150, 410, 200, 55, "Back")
    start.draw(screen, font)
    back.draw(screen, font)

    draw_text(screen, "Press Enter to start", small_font, WHITE, WIDTH // 2, 510)
    return start, back, box


def draw_settings():
    screen.fill((25, 25, 25))
    draw_text(screen, "SETTINGS", big_font, WHITE, WIDTH // 2, 80)

    sound_text = "Sound: ON" if settings["sound"] else "Sound: OFF"

    buttons = [
        Button(120, 150, 260, 50, sound_text),
        Button(120, 220, 260, 50, f"Difficulty: {settings['difficulty']}"),
        Button(120, 290, 260, 50, f"Car color: {settings['car_color']}"),
        Button(120, 390, 260, 50, "Back"),
    ]

    for button in buttons:
        button.draw(screen, font)

    draw_text(screen, "Settings are saved to settings.json", small_font, WHITE, WIDTH // 2, 520)
    return buttons


def draw_leaderboard():
    screen.fill((25, 25, 25))
    draw_text(screen, "LEADERBOARD TOP 10", big_font, WHITE, WIDTH // 2, 70)

    panel = pygame.Rect(45, 120, 410, 430)
    draw_panel(screen, panel)

    entries = load_leaderboard()

    if not entries:
        draw_text(screen, "No scores yet", font, WHITE, WIDTH // 2, 330)
    else:
        y = 145
        draw_text(screen, "Rank  Name       Score  Dist", small_font, YELLOW, 70, y, center=False)
        y += 30

        for index, item in enumerate(entries, start=1):
            name = str(item.get("name", "Player"))[:9]
            score = item.get("score", 0)
            distance = item.get("distance", 0)

            line = f"{index:<5} {name:<10} {score:<6} {distance}"
            draw_text(screen, line, small_font, WHITE, 70, y, center=False)
            y += 34

    back = Button(150, 585, 200, 55, "Back")
    back.draw(screen, font)
    return back


def draw_game_over():
    global score_saved

    if game and not score_saved:
        final_name = player_name.strip() if player_name.strip() else "Player"
        add_score(final_name, game.score, game.distance, game.coins_count)
        score_saved = True

    screen.fill((25, 25, 25))

    title = "YOU FINISHED!" if game and game.win else "GAME OVER"
    color = GREEN if game and game.win else RED

    draw_text(screen, title, big_font, color, WIDTH // 2, 100)

    if game:
        draw_text(screen, f"Name: {player_name or 'Player'}", font, WHITE, WIDTH // 2, 190)
        draw_text(screen, f"Score: {int(game.score)}", font, WHITE, WIDTH // 2, 230)
        draw_text(screen, f"Distance: {int(game.distance)}", font, WHITE, WIDTH // 2, 270)
        draw_text(screen, f"Coins: {game.coins_count}", font, WHITE, WIDTH // 2, 310)

    retry = Button(150, 390, 200, 55, "Retry")
    menu = Button(150, 460, 200, 55, "Main Menu")

    retry.draw(screen, font)
    menu.draw(screen, font)

    return retry, menu


def cycle_difficulty():
    order = list(DIFFICULTIES.keys())
    index = order.index(settings["difficulty"])
    settings["difficulty"] = order[(index + 1) % len(order)]
    save_settings(settings)


def cycle_color():
    order = list(CAR_COLORS.keys())
    index = order.index(settings["car_color"])
    settings["car_color"] = order[(index + 1) % len(order)]
    save_settings(settings)


running = True

while running:
    if state == "menu":
        menu_buttons = draw_menu()

    elif state == "name":
        name_start, name_back, name_box = draw_name_screen()

    elif state == "settings":
        settings_buttons = draw_settings()

    elif state == "leaderboard":
        leaderboard_back = draw_leaderboard()

    elif state == "playing":
        game.update()
        game.draw(screen, small_font)

        if game.game_over or game.win:
            state = "game_over"

    elif state == "game_over":
        retry_button, menu_button = draw_game_over()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if state == "menu":
            if menu_buttons[0].clicked(event):
                state = "name"
            elif menu_buttons[1].clicked(event):
                state = "leaderboard"
            elif menu_buttons[2].clicked(event):
                state = "settings"
            elif menu_buttons[3].clicked(event):
                running = False

        elif state == "name":
            if event.type == pygame.MOUSEBUTTONDOWN:
                name_active = name_box.collidepoint(event.pos)

            if event.type == pygame.KEYDOWN and name_active:
                if event.key == pygame.K_BACKSPACE:
                    player_name = player_name[:-1]
                elif event.key == pygame.K_RETURN:
                    new_game()
                elif len(player_name) < 12 and event.unicode.isprintable():
                    player_name += event.unicode

            if name_start.clicked(event):
                new_game()
            elif name_back.clicked(event):
                state = "menu"

        elif state == "settings":
            if settings_buttons[0].clicked(event):
                settings["sound"] = not settings["sound"]
                save_settings(settings)
            elif settings_buttons[1].clicked(event):
                cycle_difficulty()
            elif settings_buttons[2].clicked(event):
                cycle_color()
            elif settings_buttons[3].clicked(event):
                state = "menu"

        elif state == "leaderboard":
            if leaderboard_back.clicked(event):
                state = "menu"

        elif state == "playing":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    game.player.move_left()
                elif event.key == pygame.K_RIGHT:
                    game.player.move_right()
                elif event.key == pygame.K_ESCAPE:
                    state = "menu"

        elif state == "game_over":
            if retry_button.clicked(event):
                new_game()
            elif menu_button.clicked(event):
                state = "menu"

    pygame.display.update()
    clock.tick(60)

pygame.quit()