import sys
import subprocess
import pygame
from classes.pong_class import SoundManager


def main():
    pygame.init()

    # Define some colors
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)

    background_image = pygame.image.load("src/resources/pong_background.jpg")

    # Set the width and height of the screen
    size = (800, 600)
    screen = pygame.display.set_mode(size)

    pygame.display.set_caption("Pong")

    button_sound = pygame.mixer.Sound("src/resources/button.mp3")

    button_practice = pygame.Rect(300, 250, 200, 50)
    button_pvp = pygame.Rect(300, 325, 200, 50)
    button_exit = pygame.Rect(300, 400, 200, 50)

    def draw_text_with_shadow(
        text, size, text_x, text_y, color, shadow_color, offset=(2, 2)
    ):
        font = pygame.font.Font(pygame.font.get_default_font(), size)
        text_surface = font.render(text, True, color)
        shadow_surface = font.render(text, True, shadow_color)
        text_rect = text_surface.get_rect()
        shadow_rect = shadow_surface.get_rect()
        text_rect.center = (text_x, text_y)
        shadow_rect.center = (text_x + offset[0], text_y + offset[1])
        screen.blit(shadow_surface, shadow_rect)
        screen.blit(text_surface, text_rect)

    def open_file(file_name):
        subprocess.Popen(["python", file_name])

    # Main loop
    done = False
    while not done:
        # --- Event Processing ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Check if the user clicked on any of the buttons
                if button_practice.collidepoint(event.pos):
                    button_sound.play()
                    open_file("src/pong_practice.py")
                    print("Starting practice mode...")
                elif button_pvp.collidepoint(event.pos):
                    button_sound.play()
                    open_file("src/pong_pvp.py")
                    print("Starting PvP mode...")
                elif button_exit.collidepoint(event.pos):
                    # Exit the game
                    button_sound.play()
                    done = True

        # --- Drawing ---
        # Clear the screen
        screen.blit(background_image, (0, 0))

        # Draw the text
        pygame.draw.rect(screen, (255, 174, 67), button_practice)
        pygame.draw.rect(screen, (255, 174, 67), button_pvp)
        pygame.draw.rect(screen, (255, 174, 67), button_exit)

        draw_text_with_shadow("Practice", 24, 400, 275, WHITE, (100, 100, 100))
        draw_text_with_shadow("PvP", 24, 400, 350, WHITE, (100, 100, 100))
        draw_text_with_shadow("Exit", 24, 400, 425, WHITE, (100, 100, 100))
        draw_text_with_shadow("Pong", 48, 400, 150, WHITE, (100, 100, 100))

        # Update the screen
        pygame.display.flip()

    # Close the window and quit
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
