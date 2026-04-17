import pygame
import os


WIDTH = 900
HEIGHT = 500


BG_COLOR = (24, 26, 32)
CARD_COLOR = (39, 43, 54)
ACCENT_COLOR = (88, 166, 255)
TEXT_COLOR = (240, 240, 240)
SUBTEXT_COLOR = (180, 180, 180)
GREEN = (80, 200, 120)
RED = (220, 80, 80)
GRAY = (90, 90, 90)


def draw_text(screen, text, font, color, x, y):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))


def draw_button(screen, rect, text, font, bg_color, text_color):
    pygame.draw.rect(screen, bg_color, rect, border_radius=12)
    pygame.draw.rect(screen, ACCENT_COLOR, rect, 2, border_radius=12)

    text_surface = font.render(text, True, text_color)
    text_rect = text_surface.get_rect(center=rect.center)
    screen.blit(text_surface, text_rect)


def run_player():
    pygame.init()
    pygame.mixer.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Music Player")

    clock = pygame.time.Clock()

    
    title_font = pygame.font.SysFont("Arial", 40, bold=True)
    track_font = pygame.font.SysFont("Arial", 28, bold=True)
    info_font = pygame.font.SysFont("Arial", 22)
    small_font = pygame.font.SysFont("Arial", 18)

    current_dir = os.path.dirname(__file__)
    music_folder = os.path.join(current_dir, "music")

    
    playlist = []
    for file in os.listdir(music_folder):
        if file.endswith(".mp3") or file.endswith(".wav"):
            playlist.append(file)

    playlist.sort()

    if not playlist:
        print("No music files found in the music folder.")
        pygame.quit()
        return

    current_track = 0
    is_playing = False
    track_start_time = 0

    def load_and_play(index):
        nonlocal is_playing, track_start_time
        track_path = os.path.join(music_folder, playlist[index])
        pygame.mixer.music.load(track_path)
        pygame.mixer.music.play()
        is_playing = True
        track_start_time = pygame.time.get_ticks()

    running = True
    while running:
        screen.fill(BG_COLOR)

        
        card_rect = pygame.Rect(70, 60, 760, 300)
        pygame.draw.rect(screen, CARD_COLOR, card_rect, border_radius=20)
        pygame.draw.rect(screen, ACCENT_COLOR, card_rect, 2, border_radius=20)

        
        draw_text(screen, "Music Player", title_font, TEXT_COLOR, 320, 90)

        
        track_box = pygame.Rect(120, 160, 660, 70)
        pygame.draw.rect(screen, BG_COLOR, track_box, border_radius=14)
        pygame.draw.rect(screen, ACCENT_COLOR, track_box, 2, border_radius=14)

        draw_text(screen, "Current track:", info_font, SUBTEXT_COLOR, 145, 175)
        draw_text(screen, playlist[current_track], track_font, TEXT_COLOR, 300, 170)

        
        status_text = "Playing" if is_playing else "Stopped"
        status_color = GREEN if is_playing else RED
        draw_text(screen, "Status:", info_font, SUBTEXT_COLOR, 145, 255)
        draw_text(screen, status_text, info_font, status_color, 225, 255)

        
        draw_text(
            screen,
            f"Track {current_track + 1} of {len(playlist)}",
            info_font,
            SUBTEXT_COLOR,
            500,
            255
        )

        
        progress_bar_x = 145
        progress_bar_y = 305
        progress_bar_width = 590
        progress_bar_height = 18

        pygame.draw.rect(
            screen,
            GRAY,
            (progress_bar_x, progress_bar_y, progress_bar_width, progress_bar_height),
            border_radius=9
        )

        
        if is_playing:
            elapsed_ms = pygame.time.get_ticks() - track_start_time
            elapsed_seconds = elapsed_ms / 1000

            
            progress_ratio = min(elapsed_seconds / 30, 1.0)
        else:
            progress_ratio = 0

        pygame.draw.rect(
            screen,
            ACCENT_COLOR,
            (
                progress_bar_x,
                progress_bar_y,
                int(progress_bar_width * progress_ratio),
                progress_bar_height
            ),
            border_radius=9
        )

        
        button_font = pygame.font.SysFont("Arial", 20, bold=True)

        draw_button(screen, pygame.Rect(120, 390, 110, 50), "P - Play", button_font, CARD_COLOR, TEXT_COLOR)
        draw_button(screen, pygame.Rect(250, 390, 110, 50), "S - Stop", button_font, CARD_COLOR, TEXT_COLOR)
        draw_button(screen, pygame.Rect(380, 390, 110, 50), "N - Next", button_font, CARD_COLOR, TEXT_COLOR)
        draw_button(screen, pygame.Rect(510, 390, 140, 50), "B - Previous", button_font, CARD_COLOR, TEXT_COLOR)
        draw_button(screen, pygame.Rect(670, 390, 110, 50), "Q - Quit", button_font, CARD_COLOR, TEXT_COLOR)

        
        draw_text(
            screen,
            "Use keyboard keys to control playback",
            small_font,
            SUBTEXT_COLOR,
            320,
            460
        )

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    running = False

                elif event.key == pygame.K_p:
                    load_and_play(current_track)

                elif event.key == pygame.K_s:
                    pygame.mixer.music.stop()
                    is_playing = False

                elif event.key == pygame.K_n:
                    current_track = (current_track + 1) % len(playlist)
                    load_and_play(current_track)

                elif event.key == pygame.K_b:
                    current_track = (current_track - 1) % len(playlist)
                    load_and_play(current_track)

        clock.tick(60)

    pygame.mixer.music.stop()
    pygame.quit()