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
    """
    This class is responsible for handling all sound related operations in the game.
    It loads and plays different sound files for various game events.
    """

    def __init__(self):
        """
        Initializes the SoundManager with all the required sound files.
        """
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
        """
        Plays the sound of a paddle hit in the Pong game.
        """
        self.paddle_sound.play()
        return "Sound played"

    def play_wall_sound(self):
        """
        Plays the sound of a ball hitting the wall in the Pong game.
        """
        self.wall_sound.play()
        return "Sound played"

    def play_pong_score_sound(self):
        """
        Plays the sound of a player scoring a point in the Pong game.
        """
        self.pong_score_sound.play()
        return "Sound played"

    def play_boosted_sound(self):
        """
        Plays the sound of a boosted shot in the Pong game.
        """
        self.boosted_sound.play()
        return "Sound played"

    def play_pong_bgm_sound(self):
        """
        Plays the background music for the Pong game.
        """
        self.pong_bgm_sound = pygame.mixer.music.load("src/resources/pong_bgm.mp3")
        pygame.mixer.music.set_volume(0.25)
        pygame.mixer.music.play(-1)
        return "Bgm played"

    def play_button_sound(self):
        """
        Plays the sound of a button click in the game menu.
        """
        self.button_sound.play()
        return "Sound played"

    def play_jump_sound(self):
        """
        Plays the sound of a player making a long jump.
        """
        self.jump_sound.play()
        return "Sound played"

    def play_longjump_score_sound(self):
        """
        Plays the sound of a player scoring in the Long Jump game.
        """
        self.longjump_score_sound.play()
        return "Sound played"

    def play_longjump_bgm_sound(self):
        """
        Plays the background music for the Long Jump game.
        """
        self.longjump_bgm_sound = pygame.mixer.music.load(
            "src/resources/longjump_bgm.mp3"
        )
        pygame.mixer.music.set_volume(0.25)
        pygame.mixer.music.play(-1)
        return "Bgm played"

    def play_menu_bgm_sound(self):
        """
        Plays the background music for the game menu.
        """
        self.longjump_bgm_sound = pygame.mixer.music.load("src/resources/bgm.mp3")
        pygame.mixer.music.set_volume(0.25)
        pygame.mixer.music.play(-1)
        return "Bgm played"


def create_text_surface(text, size, color):
    """
    Creates a pygame.Surface object of the given text.
    The size and color of the text can also be specified.
    """
    font = pygame.font.Font(pygame.font.get_default_font(), size)
    text_surface = font.render(text, True, color)
    return text_surface


def create_shadow_surface(text, size, shadow_color):
    """
    Creates a pygame.Surface object of the given text that acts as a shadow.
    The size and shadow_color of the text can also be specified.
    """
    font = pygame.font.Font(pygame.font.get_default_font(), size)
    shadow_surface = font.render(text, True, shadow_color)
    return shadow_surface


def draw_text_with_shadow(
    text, size, object_x, object_y, color, shadow_color, offset=(2, 2)
):
    """
    This function renders a text string onto the screen at the specified location.
    It also creates a shadow effect for the text by first rendering the shadow and then the text itself.
    """
    text_surface = create_text_surface(text, size, color)
    shadow_surface = create_shadow_surface(text, size, shadow_color)

    text_rect = text_surface.get_rect()
    shadow_rect = shadow_surface.get_rect()

    text_rect.center = (object_x, object_y)
    shadow_rect.center = (object_x + offset[0], object_y + offset[1])

    screen.blit(shadow_surface, shadow_rect)
    screen.blit(text_surface, text_rect)


def start_game(command):
    """
    This function stops the current background music, executes the given command to start a game mode,
    and then restarts the background music. The command is expected to be a list of strings that forms a valid system command.
    """
    pygame.mixer.music.stop()
    os.system(" ".join(command))
    pygame.mixer.music.play(-1)


class Button:
    """
    This class represents a clickable button in the game.
    It has methods to check if it was clicked and to draw itself on the screen.
    """

    def __init__(self, object_x, object_y, object_w, object_h, sound_manager):
        """
        Initializes a Button object at the specified screen position.
        The dimensions of the button and the SoundManager are also specified.
        """
        self.rect = pygame.Rect(object_x, object_y, object_w, object_h)
        self.sound_manager = sound_manager

    def collidepoint(self, point):
        """
        Checks if a given point is within the bounds of the button.
        """
        return self.rect.collidepoint(point)

    def draw(
        self, screen, text, text_size, text_color, shadow_color, bg_color=(255, 174, 67)
    ):
        """
        Draws the button on the screen with the specified text.
        The size, color of the text, and the background color of the button can also be specified.
        """
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
        """
        Draws an exit button on the screen.
        """

        button_width, button_height = 40, 40
        exit_button = pygame.Rect(
            800 - button_width - 10, 10, button_width, button_height
        )
        pygame.draw.rect(screen, FONT_COLOR, exit_button, 3)
        pygame.draw.line(
            screen,
            FONT_COLOR,
            (exit_button.left + 10, exit_button.top + 10),
            (exit_button.right - 10, exit_button.bottom - 10),
            3,
        )
        pygame.draw.line(
            screen,
            FONT_COLOR,
            (exit_button.left + 10, exit_button.bottom - 10),
            (exit_button.right - 10, exit_button.top + 10),
            3,
        )

        return exit_button

    def clicked(self, click, command):
        """
        Checks if the button has been clicked. If it has, it plays a sound and executes the specified command.
        """
        m_x, m_y = pygame.mouse.get_pos()
        if self.collidepoint((m_x, m_y)):
            if click:
                self.sound_manager.play_button_sound()
                command()
