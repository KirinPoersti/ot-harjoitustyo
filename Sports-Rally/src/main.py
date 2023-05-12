import sys
import subprocess
import pygame

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FONT_COLOR = (255, 255, 255)
FPS = 60

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Sports Rally")
clock = pygame.time.Clock()

FONT = pygame.font.Font(pygame.font.get_default_font(), 32)

# Background image
background_image = pygame.image.load("src/resources/background.jpg")

# Background music
pygame.mixer.init()
pygame.mixer.music.load("src/resources/bgm.mp3")
pygame.mixer.music.set_volume(0.25)
pygame.mixer.music.play(-1)


def draw_text_with_shadow(
    text, size, object_x, object_y, color, shadow_color, offset=(2, 2)
):
    font = pygame.font.Font(pygame.font.get_default_font(), size)
    text_surface = font.render(text, True, color)
    shadow_surface = font.render(text, True, shadow_color)
    text_rect = text_surface.get_rect()
    shadow_rect = shadow_surface.get_rect()
    text_rect.center = (object_x, object_y)
    shadow_rect.center = (object_x + offset[0], object_y + offset[1])
    screen.blit(shadow_surface, shadow_rect)
    screen.blit(text_surface, text_rect)


def main_menu():
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

        button_sound = pygame.mixer.Sound("src/resources/button.mp3")

        mx, my = pygame.mouse.get_pos()

        button_long_jump = pygame.Rect(300, 250, 200, 50)
        button_pong = pygame.Rect(300, 325, 200, 50)
        button_exit = pygame.Rect(300, 400, 200, 50)

        if button_long_jump.collidepoint((mx, my)):
            if click:
                button_sound.play()
                subprocess.Popen(["python", "-m", "src.longjump.longjump_main"])
                break
        if button_pong.collidepoint((mx, my)):
            if click:
                button_sound.play()
                subprocess.Popen(["python", "-m", "src.pong.pong_main"])
                break
        if button_exit.collidepoint((mx, my)):
            if click:
                button_sound.play()
                pygame.quit()
                sys.exit()

        pygame.draw.rect(screen, (255, 174, 67), button_long_jump)
        pygame.draw.rect(screen, (255, 174, 67), button_pong)
        pygame.draw.rect(screen, (255, 174, 67), button_exit)

        draw_text_with_shadow("Long Jump", 24, 400, 275, FONT_COLOR, (100, 100, 100))
        draw_text_with_shadow("Pong", 24, 400, 350, FONT_COLOR, (100, 100, 100))
        draw_text_with_shadow("Exit", 24, 400, 425, FONT_COLOR, (100, 100, 100))
        draw_text_with_shadow("Sports Rally", 48, 400, 150, FONT_COLOR, (100, 100, 100))

        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    main_menu()
