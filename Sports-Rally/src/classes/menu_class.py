import os
import pygame

pygame.font.init()
pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FONT_COLOR = (255, 255, 255)
FPS = 60
FONT = pygame.font.Font(pygame.font.get_default_font(), 32)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


class SoundManager:
    def __init__(self):
        pygame.mixer.init()
        self.paddle_sound = pygame.mixer.Sound("src/resources/pong_paddle.mp3")
        self.wall_sound = pygame.mixer.Sound("src/resources/pong_wall.mp3")
        self.pong_score_sound = pygame.mixer.Sound("src/resources/pong_score.mp3")
        self.boosted_sound = pygame.mixer.Sound("src/resources/pong_boosted.mp3")
        self.pong_bgm_sound = pygame.mixer.music.load("src/resources/pong_bgm.mp3")

        self.button_sound = pygame.mixer.Sound("src/resources/button.mp3")

        self.jump_sound = pygame.mixer.Sound("src/resources/longjump_jump.mp3")
        self.longjump_score_sound = pygame.mixer.Sound(
            "src/resources/longjump_score.mp3"
        )
        self.longjump_bgm_sound = pygame.mixer.music.load(
            "src/resources/longjump_bgm.mp3"
        )

    def play_paddle_sound(self):
        self.paddle_sound.play()
        return "Sound played"

    def play_wall_sound(self):
        self.wall_sound.play()
        return "Sound played"

    def play_pong_score_sound(self):
        self.pong_score_sound.play()
        return "Sound played"

    def play_boosted_sound(self):
        self.boosted_sound.play()
        return "Sound played"

    def play_pong_bgm_sound(self):
        self.pong_bgm_sound = pygame.mixer.music.load("src/resources/pong_bgm.mp3")
        pygame.mixer.music.set_volume(0.25)
        pygame.mixer.music.play(-1)
        return "Bgm played"

    def play_button_sound(self):
        self.button_sound.play()
        return "Sound played"

    def play_jump_sound(self):
        self.jump_sound.play()
        return "Sound played"

    def play_longjump_score_sound(self):
        self.longjump_score_sound.play()
        return "Sound played"

    def play_longjump_bgm_sound(self):
        self.longjump_bgm_sound = pygame.mixer.music.load(
            "src/resources/longjump_bgm.mp3"
        )
        pygame.mixer.music.set_volume(0.25)
        pygame.mixer.music.play(-1)
        return "Bgm played"

    def play_menu_bgm_sound(self):
        self.longjump_bgm_sound = pygame.mixer.music.load("src/resources/bgm.mp3")
        pygame.mixer.music.set_volume(0.25)
        pygame.mixer.music.play(-1)
        return "Bgm played"


def create_text_surface(text, size, color):
    font = pygame.font.Font(pygame.font.get_default_font(), size)
    text_surface = font.render(text, True, color)
    return text_surface


def create_shadow_surface(text, size, shadow_color):
    font = pygame.font.Font(pygame.font.get_default_font(), size)
    shadow_surface = font.render(text, True, shadow_color)
    return shadow_surface


def draw_text_with_shadow(
    text, size, object_x, object_y, color, shadow_color, offset=(2, 2)
):
    text_surface = create_text_surface(text, size, color)
    shadow_surface = create_shadow_surface(text, size, shadow_color)

    text_rect = text_surface.get_rect()
    shadow_rect = shadow_surface.get_rect()

    text_rect.center = (object_x, object_y)
    shadow_rect.center = (object_x + offset[0], object_y + offset[1])

    screen.blit(shadow_surface, shadow_rect)
    screen.blit(text_surface, text_rect)


def start_game(command):
    pygame.mixer.music.stop()
    os.system(" ".join(command))
    pygame.mixer.music.play(-1)


class Button:
    def __init__(self, object_x, object_y, object_w, object_h, sound_manager):
        self.rect = pygame.Rect(object_x, object_y, object_w, object_h)
        self.sound_manager = sound_manager

    def collidepoint(self, point):
        return self.rect.collidepoint(point)

    def draw(
        self, screen, text, text_size, text_color, shadow_color, bg_color=(255, 174, 67)
    ):
        pygame.draw.rect(screen, bg_color, self.rect)
        draw_text_with_shadow(
            text,
            text_size,
            self.rect.centerx,
            self.rect.centery,
            text_color,
            shadow_color,
        )

    def draw_exit_button(self, screen):
        white_color = (255, 255, 255)

        button_width, button_height = 40, 40
        exit_button = pygame.Rect(
            800 - button_width - 10, 10, button_width, button_height
        )
        pygame.draw.rect(screen, white_color, exit_button, 3)
        pygame.draw.line(
            screen,
            white_color,
            (exit_button.left + 10, exit_button.top + 10),
            (exit_button.right - 10, exit_button.bottom - 10),
            3,
        )
        pygame.draw.line(
            screen,
            white_color,
            (exit_button.left + 10, exit_button.bottom - 10),
            (exit_button.right - 10, exit_button.top + 10),
            3,
        )

        return exit_button

    def clicked(self, click, command):
        m_x, m_y = pygame.mouse.get_pos()
        if self.collidepoint((m_x, m_y)):
            if click:
                self.sound_manager.play_button_sound()
                command()
