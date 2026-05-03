import random
import pygame

WIDTH = 500
HEIGHT = 700

LANES = [120, 230, 340]

# Увеличенная дистанция
DIFFICULTIES = {
    "easy": {"speed": 4, "spawn": 80, "goal": 8000},
    "medium": {"speed": 5, "spawn": 60, "goal": 12000},
    "hard": {"speed": 6, "spawn": 40, "goal": 16000},
}

CAR_COLORS = {
    "green": (0, 255, 0),
    "blue": (0, 150, 255),
    "red": (255, 0, 0),
    "yellow": (255, 255, 0),
}


class Player:
    def __init__(self, color):
        self.lane = 1
        self.width = 40
        self.height = 60
        self.y = HEIGHT - 100
        self.color = CAR_COLORS[color]

    @property
    def rect(self):
        return pygame.Rect(LANES[self.lane] - 20, self.y, self.width, self.height)

    def move_left(self):
        if self.lane > 0:
            self.lane -= 1

    def move_right(self):
        if self.lane < 2:
            self.lane += 1

    def draw(self, screen):
        r = self.rect

        pygame.draw.rect(screen, self.color, r, border_radius=8)

        # стекло
        pygame.draw.rect(screen, (200, 200, 255), (r.x+8, r.y+8, 24, 20), border_radius=5)

        # фары
        pygame.draw.circle(screen, (255,255,0), (r.x+5, r.y+5), 4)
        pygame.draw.circle(screen, (255,255,0), (r.x+35, r.y+5), 4)

        # колёса
        pygame.draw.circle(screen, (0,0,0), (r.x+5, r.y+50), 5)
        pygame.draw.circle(screen, (0,0,0), (r.x+35, r.y+50), 5)


class Enemy:
    def __init__(self, speed):
        self.lane = random.randint(0, 2)
        self.y = -60
        self.speed = speed

    @property
    def rect(self):
        return pygame.Rect(LANES[self.lane] - 20, self.y, 40, 60)

    def update(self, speed):
        self.y += speed

    def draw(self, screen):
        r = self.rect

        pygame.draw.rect(screen, (255, 0, 0), r, border_radius=8)
        pygame.draw.rect(screen, (200,200,255), (r.x+8, r.y+8, 24, 20), border_radius=5)

        pygame.draw.circle(screen, (255,0,0), (r.x+5, r.y+55), 4)
        pygame.draw.circle(screen, (255,0,0), (r.x+35, r.y+55), 4)


class Coin:
    def __init__(self, speed):
        self.lane = random.randint(0, 2)
        self.y = -30
        self.speed = speed
        self.value = random.choice([1, 5, 10])

    @property
    def rect(self):
        return pygame.Rect(LANES[self.lane] - 10, self.y, 20, 20)

    def update(self, speed):
        self.y += speed

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 215, 0), self.rect.center, 10)


class PowerUp:
    def __init__(self, speed):
        self.lane = random.randint(0, 2)
        self.y = -30
        self.speed = speed
        self.type = random.choice(["nitro", "shield", "repair"])

    @property
    def rect(self):
        return pygame.Rect(LANES[self.lane] - 15, self.y, 30, 30)

    def update(self, speed):
        self.y += speed

    def draw(self, screen):
        color = (0, 0, 255) if self.type == "nitro" else (255, 0, 255) if self.type == "shield" else (0, 255, 0)
        pygame.draw.rect(screen, color, self.rect, border_radius=6)


class Game:
    def __init__(self, settings):
        self.settings = settings
        self.config = DIFFICULTIES[settings["difficulty"]]

        self.player = Player(settings["car_color"])
        self.enemies = []
        self.coins = []
        self.powerups = []

        self.score = 0
        self.distance = 0
        self.coins_count = 0

        self.base_speed = self.config["speed"]
        self.goal = self.config["goal"]

        self.game_over = False
        self.win = False

        self.active_power = None
        self.power_timer = 0

        self.frame = 0

        # анимация дороги
        self.road_offset = 0

        # тряска
        self.shake = 0

    def spawn(self):
        if self.frame % self.config["spawn"] == 0:
            self.enemies.append(Enemy(self.base_speed))

        if self.frame % 50 == 0:
            self.coins.append(Coin(self.base_speed))

        if self.frame % 200 == 0:
            self.powerups.append(PowerUp(self.base_speed))

    def update(self):
        if self.game_over or self.win:
            return

        self.frame += 1

        # ускорение со временем
        self.base_speed += 0.0005

        speed = self.base_speed

        if self.active_power == "nitro":
            speed *= 1.7

        self.road_offset += speed
        if self.road_offset > 80:
            self.road_offset = 0

        self.spawn()

        for e in self.enemies:
            e.update(speed)

        for c in self.coins:
            c.update(speed)

        for p in self.powerups:
            p.update(speed)

        self.enemies = [e for e in self.enemies if e.y < HEIGHT]
        self.coins = [c for c in self.coins if c.y < HEIGHT]
        self.powerups = [p for p in self.powerups if p.y < HEIGHT]

        # столкновения
        for e in self.enemies:
            if self.player.rect.colliderect(e.rect):
                if self.active_power == "shield":
                    self.active_power = None
                else:
                    self.game_over = True
                    self.shake = 10

        for c in self.coins[:]:
            if self.player.rect.colliderect(c.rect):
                self.coins_count += c.value
                self.score += c.value * 10
                self.coins.remove(c)

        for p in self.powerups[:]:
            if self.player.rect.colliderect(p.rect):
                self.active_power = p.type
                self.power_timer = 180
                self.powerups.remove(p)

        if self.active_power:
            self.power_timer -= 1
            if self.power_timer <= 0:
                self.active_power = None

        self.distance += speed * 0.5
        self.score += 1

        if self.distance >= self.goal:
            self.win = True

    def draw(self, screen, font):
        offset_x = random.randint(-self.shake, self.shake)
        offset_y = random.randint(-self.shake, self.shake)

        if self.shake > 0:
            self.shake -= 1

        # фон
        screen.fill((20, 120, 50))

        # дорога
        pygame.draw.rect(screen, (40,40,40), (80, 0, 340, HEIGHT))

        pygame.draw.line(screen, (255,255,0), (80,0), (80,HEIGHT), 4)
        pygame.draw.line(screen, (255,255,0), (420,0), (420,HEIGHT), 4)

        for y in range(-80, HEIGHT, 80):
            pygame.draw.line(screen, (255,255,255), (200, y + self.road_offset), (200, y + 40 + self.road_offset), 4)
            pygame.draw.line(screen, (255,255,255), (300, y + self.road_offset), (300, y + 40 + self.road_offset), 4)

        # объекты
        for e in self.enemies:
            e.draw(screen)

        for c in self.coins:
            c.draw(screen)

        for p in self.powerups:
            p.draw(screen)

        self.player.draw(screen)

        # HUD
        screen.blit(font.render(f"Score: {int(self.score)}", True, (255,255,255)), (10,10))
        screen.blit(font.render(f"Coins: {self.coins_count}", True, (255,255,255)), (10,40))
        screen.blit(font.render(f"Distance: {int(self.distance)}", True, (255,255,255)), (10,70))