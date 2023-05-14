import sys
import subprocess
import pygame
from ..classes.menu_class import SoundManager, Button, draw_text_with_shadow

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FONT_COLOR = (255, 255, 255)
FPS = 60

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Long Jump")
clock = pygame.time.Clock()

background_image = pygame.image.load("src/resources/longjump_background.jpg")


def main_menu():
    """
    The main function to start the main menu loop of the game.

    Raises:
        SystemExit: Exits the game menu when the loop ends or the "Exit" button is clicked.

    This function initializes the sound manager and buttons for
    "Play", "Leaderboard", and "Exit".
    It enters a loop that continues until a quit event.
    Within the loop, the function checks for mouse button down events
    to handle button clicks and updates the screen with the background image, title,
    and buttons. It also checks if any button is clicked and performs the corresponding action.
    """
    sound_manager = SoundManager()
    button_play = Button(300, 250, 200, 50, sound_manager)
    button_leaderboard = Button(300, 325, 200, 50, sound_manager)
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

        draw_text_with_shadow("Long Jump", 48, 400, 150, FONT_COLOR, (100, 100, 100))

        button_play.draw(screen, "Play", 24, FONT_COLOR, (100, 100, 100))
        button_leaderboard.draw(screen, "Leaderboard", 24, FONT_COLOR, (100, 100, 100))
        button_exit.draw(screen, "Exit", 24, FONT_COLOR, (100, 100, 100))

        button_play.clicked(
            click,
            lambda: subprocess.Popen(["python", "-m", "src.longjump.longjump"]),
        )
        button_leaderboard.clicked(
            click,
            lambda: subprocess.Popen(
                ["python", "-m", "src.longjump.longjump_leaderboard"]
            ),
        )
        button_exit.clicked(click, lambda: pygame.quit() or sys.exit())

        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    main_menu()
