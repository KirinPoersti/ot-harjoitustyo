import sys
import pygame
from ..classes.menu_class import SoundManager
from ..classes.pong_class import Paddle, Ball, StaminaSystem, GameObjects

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FONT_COLOR = (255, 255, 255)
FPS = 60
font = pygame.font.Font(None, 36)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pong Practice")
clock = pygame.time.Clock()

sound_manager = SoundManager()

player_paddle = Paddle(100, SCREEN_HEIGHT // 2 - 100 // 2, 20, 100, SCREEN_HEIGHT)
ball = Ball(SCREEN_WIDTH, SCREEN_HEIGHT, 15, 5, sound_manager, practice_mode=True)

PLAYER_SCORE = 0

stamina_system = StaminaSystem(800, 600, 1000, 300, 5, display_mode="left")

game_objects = GameObjects(
    SCREEN_WIDTH, SCREEN_HEIGHT, player_paddle, ball, stamina_system
)

while True:
    clock.tick(FPS)
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        stamina_system.update_stamina(event, keys)

    PLAYER_BOOST_ACTIVE = stamina_system.boost_active

    player_paddle.move_paddle(keys, not PLAYER_BOOST_ACTIVE)
    PLAYER_SCORE, _ = ball.move_ball_practice(player_paddle, PLAYER_SCORE, 0)

    screen.fill((0, 0, 0))

    game_objects.draw_practice(screen, PLAYER_SCORE, stamina_system)

    pygame.display.flip()
