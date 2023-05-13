import sys
import pygame
from .longjump import load_scores
from ..classes.menu_class import Button, SoundManager

sound_manager = SoundManager()
pygame.init()


def main():
    white_color = (255, 255, 255)

    size = (800, 600)
    screen = pygame.display.set_mode(size)

    pygame.display.set_caption("Leaderboard")

    leaderboard_file = "src/resources/leaderboard.csv"

    def display_leaderboard():
        scores = load_scores(leaderboard_file)
        scores.sort(key=lambda x: x[1], reverse=True)

        screen.fill((0, 0, 0))

        font = pygame.font.Font(None, 36)
        text_color = white_color

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