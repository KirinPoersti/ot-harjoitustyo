import pygame
from .longjump import load_scores


pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FONT_COLOR = (255, 255, 255)
FPS = 60


def main():
    """
    The main function to start the leaderboard display loop.

    Raises:
        SystemExit: Exits the leaderboard display when the loop ends.

    This function initializes the display, sets the caption,
    and enters a loop that continues until a quit or escape event.
    Within the loop, the function calls display_leaderboard() to update the display,
    and then flips the display to make the updates visible.
    """
    size = (SCREEN_WIDTH, SCREEN_HEIGHT)
    screen = pygame.display.set_mode(size)

    pygame.display.set_caption("Leaderboard")

    leaderboard_file = "src/resources/leaderboard.csv"

    def display_leaderboard():
        """
        Displays the leaderboard on the screen.

        This function loads the scores from the leaderboard file,
        sorts them in descending order, and then displays the top 10 scores
        on the screen. The score display includes the player's rank, name, and score.
        """
        scores = load_scores(leaderboard_file)
        scores.sort(key=lambda x: x[1], reverse=True)

        screen.fill((0, 0, 0))

        font = pygame.font.Font(None, 36)
        text_color = FONT_COLOR

        for i, (player_name, score) in enumerate(scores[:10]):
            text = font.render(f"{i + 1}. {player_name}: {score}m", True, text_color)
            screen.blit(text, (325, 85 + i * 40))

    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    done = True

        display_leaderboard()
        pygame.display.flip()
    pygame.quit()


if __name__ == "__main__":
    main()
