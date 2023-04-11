
import sys
import pygame
import subprocess

def main():
    pygame.init()

    # Define some colors
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)

    # Set the width and height of the screen
    size = (800, 600)
    screen = pygame.display.set_mode(size)

    pygame.display.set_caption("Pong Menu")

    # Create font objects
    font = pygame.font.SysFont('Calibri', 50)
    small_font = pygame.font.SysFont('Calibri', 30)

    # Create text objects
    title_text = font.render("PONG", True, WHITE)
    practice_text = small_font.render("Practice Mode", True, WHITE)
    pvp_text = small_font.render("PvP", True, WHITE)
    exit_text = small_font.render("Exit", True, WHITE)

    # Create rectangle objects for the text
    title_rect = title_text.get_rect()
    title_rect.center = (screen.get_width() // 2, 100)

    practice_rect = practice_text.get_rect()
    practice_rect.center = (screen.get_width() // 2, 250)

    pvp_rect = pvp_text.get_rect()
    pvp_rect.center = (screen.get_width() // 2, 325)

    exit_rect = exit_text.get_rect()
    exit_rect.center = (screen.get_width() // 2, 400)

    def open_file(file_name):
        subprocess.Popen(['py', file_name])

    # Main loop
    done = False
    while not done:
        # --- Event Processing ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Check if the user clicked on any of the buttons
                if practice_rect.collidepoint(event.pos):
                    open_file('pong_practice.py')
                    print("Starting practice mode...")
                elif pvp_rect.collidepoint(event.pos):
                    open_file('pong_main.py')
                    print("Starting PvP mode...")
                elif exit_rect.collidepoint(event.pos):
                    # Exit the game
                    done = True

        # --- Drawing ---
        # Clear the screen
        screen.fill(BLACK)

        # Draw the text
        screen.blit(title_text, title_rect)
        screen.blit(practice_text, practice_rect)
        screen.blit(pvp_text, pvp_rect)
        screen.blit(exit_text, exit_rect)

        # Update the screen
        pygame.display.flip()

    # Close the window and quit
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
