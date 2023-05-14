import sys
import threading
import pygame
from .classes.menu_class import SoundManager, Button, draw_text_with_shadow, start_game

pygame.font.init()
pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FONT_COLOR = (255, 255, 255)
FPS = 60

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Sports Rally")
clock = pygame.time.Clock()

FONT = pygame.font.Font(pygame.font.get_default_font(), 32)

background_image = pygame.image.load("src/resources/background.jpg")


def main_menu():
    """
    This function initializes the main menu of the game.
    It creates the buttons for different game modes and handles the click events to
    start the selected game mode or to exit the game.
    """
    sound_manager = SoundManager()
    sound_manager.play_menu_bgm_sound()
    button_long_jump = Button(300, 250, 200, 50, sound_manager)
    button_pong = Button(300, 325, 200, 50, sound_manager)
    button_exit = Button(300, 400, 200, 50, sound_manager)

    while True:
        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        screen.blit(background_image, (0, 0))

        draw_text_with_shadow("Sports Rally", 48, 400, 150, FONT_COLOR, (100, 100, 100))

        button_long_jump.draw(screen, "Long Jump", 24, FONT_COLOR, (100, 100, 100))
        button_pong.draw(screen, "Pong", 24, FONT_COLOR, (100, 100, 100))
        button_exit.draw(screen, "Exit", 24, FONT_COLOR, (100, 100, 100))

        if button_long_jump.clicked(
            click,
            lambda: threading.Thread(
                target=start_game,
                args=(["python", "-m", "src.longjump.longjump_main"],),
            ).start(),
        ):
            pygame.display.quit()

        if button_pong.clicked(
            click,
            lambda: threading.Thread(
                target=start_game, args=(["python", "-m", "src.pong.pong_main"],)
            ).start(),
        ):
            pygame.display.quit()

        if button_exit.clicked(click, lambda: pygame.quit() or sys.exit()):
            pass

        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    main_menu()
