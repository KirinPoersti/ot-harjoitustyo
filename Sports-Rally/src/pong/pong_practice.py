import sys
import pygame
from ..classes.menu_class import SoundManager
from ..classes.pong_class import Paddle, Ball, StaminaSystem, GameObjects

pygame.init()

WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
font = pygame.font.Font(None, 36)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong Practice")
clock = pygame.time.Clock()
FPS = 60

sound_manager = SoundManager()

player_paddle = Paddle(100, HEIGHT // 2 - 100 // 2, 20, 100, HEIGHT)
ball = Ball(WIDTH, HEIGHT, 15, 5, sound_manager, practice_mode=True)

PLAYER_SCORE = 0

stamina_system = StaminaSystem(800, 600, 1000, 300, 5, display_mode="left")

game_objects = GameObjects(WIDTH, HEIGHT, player_paddle, ball, stamina_system)

button_width, button_height = 40, 40
exit_button = pygame.Rect(WIDTH - button_width - 10, 10, button_width, button_height)

while True:
    clock.tick(FPS)
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if exit_button.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()
        stamina_system.update_stamina(event, keys)

    player_boost_active = stamina_system.boost_active

    player_paddle.move_paddle(keys, not player_boost_active)
    PLAYER_SCORE, _ = ball.move_ball_practice(player_paddle, PLAYER_SCORE, 0)

    screen.fill((0, 0, 0))

    game_objects.draw_practice(screen, PLAYER_SCORE, stamina_system)

    pygame.display.flip()
