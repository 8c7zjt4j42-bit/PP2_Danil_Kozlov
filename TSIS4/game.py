import pygame
import random
import json
import os
from config import *
from db import save_result, get_leaderboard, get_personal_best


class SnakeGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("TSIS4 Snake Game")
        self.clock = pygame.time.Clock()

        self.font = pygame.font.SysFont("Arial", 26)
        self.small_font = pygame.font.SysFont("Arial", 20)
        self.big_font = pygame.font.SysFont("Arial", 42)

        self.username = ""
        self.settings = self.load_settings()
        self.state = "menu"

        self.reset_game()

    def load_settings(self):
        if not os.path.exists("settings.json"):
            return {
                "snake_color": list(GREEN),
                "grid": True,
                "sound": False
            }

        with open("settings.json", "r") as file:
            return json.load(file)

    def save_settings(self):
        with open("settings.json", "w") as file:
            json.dump(self.settings, file, indent=4)

    def reset_game(self):
        self.snake = [(WIDTH // 2, HEIGHT // 2)]
        self.direction = (CELL_SIZE, 0)
        self.next_direction = self.direction

        self.score = 0
        self.level = 1
        self.speed = FPS

        # ВАЖНО: obstacles должен быть создан ДО random_position()
        self.obstacles = []

        self.food = self.random_position()
        self.food_value = random.choice([1, 2, 3])
        self.food_spawn_time = pygame.time.get_ticks()

        self.poison = self.random_position()
        self.power_up = None
        self.power_up_type = None
        self.power_up_spawn_time = 0

        self.active_power = None
        self.active_power_end = 0
        self.shield = False

        if self.username:
            self.personal_best = get_personal_best(self.username)
        else:
            self.personal_best = 0

    def draw_text(self, text, font, color, x, y, center=False):
        img = font.render(text, True, color)
        rect = img.get_rect()

        if center:
            rect.center = (x, y)
        else:
            rect.topleft = (x, y)

        self.screen.blit(img, rect)

    def random_position(self):
        while True:
            x = random.randrange(0, WIDTH, CELL_SIZE)
            y = random.randrange(0, HEIGHT, CELL_SIZE)
            pos = (x, y)

            if (
                pos not in self.snake
                and pos not in self.obstacles
                and pos != getattr(self, "food", None)
                and pos != getattr(self, "poison", None)
            ):
                return pos

    def generate_obstacles(self):
        self.obstacles = []

        if self.level < 3:
            return

        count = self.level + 2

        for _ in range(count):
            pos = self.random_position()

            head_x, head_y = self.snake[0]

            near_head = (
                abs(pos[0] - head_x) <= CELL_SIZE * 2
                and abs(pos[1] - head_y) <= CELL_SIZE * 2
            )

            if not near_head:
                self.obstacles.append(pos)

    def spawn_food(self):
        self.food = self.random_position()
        self.food_value = random.choice([1, 2, 3])
        self.food_spawn_time = pygame.time.get_ticks()

    def spawn_power_up(self):
        if self.power_up is None and random.randint(1, 100) <= 2:
            self.power_up = self.random_position()
            self.power_up_type = random.choice(["speed", "slow", "shield"])
            self.power_up_spawn_time = pygame.time.get_ticks()

    def apply_power_up(self):
        now = pygame.time.get_ticks()

        if self.power_up_type == "speed":
            self.active_power = "speed"
            self.active_power_end = now + 5000
            self.speed += 5

        elif self.power_up_type == "slow":
            self.active_power = "slow"
            self.active_power_end = now + 5000
            self.speed = max(5, self.speed - 5)

        elif self.power_up_type == "shield":
            self.shield = True
            self.active_power = "shield"

        self.power_up = None
        self.power_up_type = None

    def update_power_up(self):
        now = pygame.time.get_ticks()

        if self.power_up and now - self.power_up_spawn_time > 8000:
            self.power_up = None
            self.power_up_type = None

        if self.active_power in ["speed", "slow"] and now > self.active_power_end:
            self.speed = FPS + self.level
            self.active_power = None

    def handle_poison(self):
        if len(self.snake) <= 2:
            self.game_over()
            return

        remove_count = min(2, len(self.snake) - 1)

        for _ in range(remove_count):
            self.snake.pop()

        self.poison = self.random_position()

    def game_over(self):
        try:
            save_result(self.username, self.score, self.level)
        except Exception as e:
            print("Database save error:", e)

        self.state = "game_over"

    def update_game(self):
        self.direction = self.next_direction

        head_x, head_y = self.snake[0]
        dx, dy = self.direction
        new_head = (head_x + dx, head_y + dy)

        hit_wall = (
            new_head[0] < 0
            or new_head[0] >= WIDTH
            or new_head[1] < 0
            or new_head[1] >= HEIGHT
        )

        hit_self = new_head in self.snake
        hit_obstacle = new_head in self.obstacles

        if hit_wall or hit_self or hit_obstacle:
            if self.shield:
                self.shield = False
                self.active_power = None
                return
            else:
                self.game_over()
                return

        self.snake.insert(0, new_head)

        if new_head == self.food:
            self.score += self.food_value

            old_level = self.level
            self.level = self.score // 5 + 1

            if self.level != old_level:
                self.speed = FPS + self.level
                self.generate_obstacles()

            self.spawn_food()

        elif new_head == self.poison:
            self.handle_poison()

        elif self.power_up and new_head == self.power_up:
            self.apply_power_up()

        else:
            self.snake.pop()

        self.spawn_power_up()
        self.update_power_up()

    def draw_grid(self):
        if not self.settings["grid"]:
            return

        for x in range(0, WIDTH, CELL_SIZE):
            pygame.draw.line(self.screen, (35, 35, 35), (x, 0), (x, HEIGHT))

        for y in range(0, HEIGHT, CELL_SIZE):
            pygame.draw.line(self.screen, (35, 35, 35), (0, y), (WIDTH, y))

    def draw_game(self):
        self.screen.fill(BLACK)
        self.draw_grid()

        for block in self.obstacles:
            pygame.draw.rect(self.screen, GRAY, (*block, CELL_SIZE, CELL_SIZE))

        pygame.draw.rect(self.screen, YELLOW, (*self.food, CELL_SIZE, CELL_SIZE))
        self.draw_text(str(self.food_value), self.small_font, BLACK, self.food[0] + 5, self.food[1])

        pygame.draw.rect(self.screen, DARK_RED, (*self.poison, CELL_SIZE, CELL_SIZE))

        if self.power_up:
            color = BLUE

            if self.power_up_type == "slow":
                color = PURPLE
            elif self.power_up_type == "shield":
                color = ORANGE

            pygame.draw.rect(self.screen, color, (*self.power_up, CELL_SIZE, CELL_SIZE))

        snake_color = tuple(self.settings["snake_color"])

        for part in self.snake:
            pygame.draw.rect(self.screen, snake_color, (*part, CELL_SIZE, CELL_SIZE))

        self.draw_text(f"User: {self.username}", self.small_font, WHITE, 10, 10)
        self.draw_text(f"Score: {self.score}", self.small_font, WHITE, 10, 35)
        self.draw_text(f"Level: {self.level}", self.small_font, WHITE, 10, 60)
        self.draw_text(f"Best: {self.personal_best}", self.small_font, WHITE, 10, 85)

        if self.active_power:
            self.draw_text(f"Power: {self.active_power}", self.small_font, WHITE, 10, 110)

    def draw_menu(self):
        self.screen.fill(BLACK)

        self.draw_text("TSIS4 Snake Game", self.big_font, GREEN, WIDTH // 2, 100, True)
        self.draw_text("Enter username:", self.font, WHITE, WIDTH // 2, 180, True)
        self.draw_text(self.username + "|", self.font, YELLOW, WIDTH // 2, 220, True)

        self.draw_text("ENTER - Play", self.font, WHITE, WIDTH // 2, 300, True)
        self.draw_text("L - Leaderboard", self.font, WHITE, WIDTH // 2, 340, True)
        self.draw_text("S - Settings", self.font, WHITE, WIDTH // 2, 380, True)
        self.draw_text("Q - Quit", self.font, WHITE, WIDTH // 2, 420, True)

    def draw_game_over(self):
        self.screen.fill(BLACK)

        self.draw_text("Game Over", self.big_font, RED, WIDTH // 2, 120, True)
        self.draw_text(f"Username: {self.username}", self.font, WHITE, WIDTH // 2, 200, True)
        self.draw_text(f"Score: {self.score}", self.font, WHITE, WIDTH // 2, 240, True)
        self.draw_text(f"Level: {self.level}", self.font, WHITE, WIDTH // 2, 280, True)
        self.draw_text(f"Personal best: {max(self.score, self.personal_best)}", self.font, YELLOW, WIDTH // 2, 320, True)

        self.draw_text("R - Retry", self.font, WHITE, WIDTH // 2, 400, True)
        self.draw_text("M - Main Menu", self.font, WHITE, WIDTH // 2, 440, True)

    def draw_leaderboard(self):
        self.screen.fill(BLACK)

        self.draw_text("Leaderboard TOP 10", self.big_font, YELLOW, WIDTH // 2, 60, True)

        try:
            data = get_leaderboard()
        except Exception as e:
            print("Leaderboard error:", e)
            data = []

        y = 130

        if not data:
            self.draw_text("No results yet", self.font, WHITE, WIDTH // 2, y, True)

        for i, row in enumerate(data, start=1):
            username, score, level, played_at = row
            date_text = played_at.strftime("%Y-%m-%d")
            text = f"{i}. {username} | Score: {score} | Level: {level} | {date_text}"
            self.draw_text(text, self.small_font, WHITE, 80, y)
            y += 35

        self.draw_text("B - Back", self.font, WHITE, WIDTH // 2, 540, True)

    def draw_settings(self):
        self.screen.fill(BLACK)

        self.draw_text("Settings", self.big_font, GREEN, WIDTH // 2, 80, True)

        grid_status = "ON" if self.settings["grid"] else "OFF"
        sound_status = "ON" if self.settings["sound"] else "OFF"

        self.draw_text(f"1 - Grid: {grid_status}", self.font, WHITE, WIDTH // 2, 180, True)
        self.draw_text(f"2 - Sound: {sound_status}", self.font, WHITE, WIDTH // 2, 230, True)
        self.draw_text("3 - Snake color: Green", self.font, GREEN, WIDTH // 2, 280, True)
        self.draw_text("4 - Snake color: Blue", self.font, BLUE, WIDTH // 2, 330, True)
        self.draw_text("5 - Snake color: Purple", self.font, PURPLE, WIDTH // 2, 380, True)
        self.draw_text("B - Save & Back", self.font, WHITE, WIDTH // 2, 470, True)

    def handle_menu_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if self.username.strip():
                    self.reset_game()
                    self.state = "game"

            elif event.key == pygame.K_BACKSPACE:
                self.username = self.username[:-1]

            elif event.key == pygame.K_l:
                self.state = "leaderboard"

            elif event.key == pygame.K_s:
                self.state = "settings"

            elif event.key == pygame.K_q:
                pygame.quit()
                exit()

            else:
                if len(self.username) < 12 and event.unicode.isprintable():
                    self.username += event.unicode

    def handle_game_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and self.direction != (0, CELL_SIZE):
                self.next_direction = (0, -CELL_SIZE)

            elif event.key == pygame.K_DOWN and self.direction != (0, -CELL_SIZE):
                self.next_direction = (0, CELL_SIZE)

            elif event.key == pygame.K_LEFT and self.direction != (CELL_SIZE, 0):
                self.next_direction = (-CELL_SIZE, 0)

            elif event.key == pygame.K_RIGHT and self.direction != (-CELL_SIZE, 0):
                self.next_direction = (CELL_SIZE, 0)

    def handle_game_over_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                self.reset_game()
                self.state = "game"

            elif event.key == pygame.K_m:
                self.state = "menu"

    def handle_leaderboard_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_b:
                self.state = "menu"

    def handle_settings_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                self.settings["grid"] = not self.settings["grid"]

            elif event.key == pygame.K_2:
                self.settings["sound"] = not self.settings["sound"]

            elif event.key == pygame.K_3:
                self.settings["snake_color"] = list(GREEN)

            elif event.key == pygame.K_4:
                self.settings["snake_color"] = list(BLUE)

            elif event.key == pygame.K_5:
                self.settings["snake_color"] = list(PURPLE)

            elif event.key == pygame.K_b:
                self.save_settings()
                self.state = "menu"

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if self.state == "menu":
                    self.handle_menu_event(event)

                elif self.state == "game":
                    self.handle_game_event(event)

                elif self.state == "game_over":
                    self.handle_game_over_event(event)

                elif self.state == "leaderboard":
                    self.handle_leaderboard_event(event)

                elif self.state == "settings":
                    self.handle_settings_event(event)

            if self.state == "menu":
                self.draw_menu()

            elif self.state == "game":
                self.update_game()
                self.draw_game()

            elif self.state == "game_over":
                self.draw_game_over()

            elif self.state == "leaderboard":
                self.draw_leaderboard()

            elif self.state == "settings":
                self.draw_settings()

            pygame.display.update()
            self.clock.tick(self.speed)