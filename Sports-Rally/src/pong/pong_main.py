import sys
import subprocess
import pygame
from ..classes.menu_class import SoundManager, Button, draw_text_with_shadow

pygame.font.init()
pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FONT_COLOR = (255, 255, 255)
FPS = 60

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pong")
clock = pygame.time.Clock()

background_image = pygame.image.load("src/resources/pong_background.jpg")


def main_menu():
    sound_manager = SoundManager()
    button_practice = Button(300, 250, 200, 50, sound_manager)
    button_pvp = Button(300, 325, 200, 50, sound_manager)
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

        draw_text_with_shadow("Pong", 48, 400, 150, FONT_COLOR, (100, 100, 100))

        button_practice.draw(screen, "Practice", 24, FONT_COLOR, (100, 100, 100))
        button_pvp.draw(screen, "PvP", 24, FONT_COLOR, (100, 100, 100))
        button_exit.draw(screen, "Exit", 24, FONT_COLOR, (100, 100, 100))

        button_practice.clicked(
            click,
            lambda: subprocess.Popen(["python", "-m", "src.pong.pong_practice"]),
        )
        button_pvp.clicked(
            click, lambda: subprocess.Popen(["python", "-m", "src.pong.pong_pvp"])
        )
        button_exit.clicked(click, lambda: pygame.quit() or sys.exit())

        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    main_menu()
