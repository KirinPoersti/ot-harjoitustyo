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
pygame.display.set_caption("Pong PvP")
clock = pygame.time.Clock()
FPS = 60

sound_manager = SoundManager()
sound_manager.play_pong_bgm_sound()

player_paddle = Paddle(100, SCREEN_HEIGHT // 2 - 100 // 2, 20, 100, SCREEN_HEIGHT)
opponent_paddle = Paddle(
    SCREEN_WIDTH - 130, SCREEN_HEIGHT // 2 - 100 // 2, 20, 100, SCREEN_HEIGHT
)
ball = Ball(SCREEN_WIDTH, SCREEN_HEIGHT, 15, 5, sound_manager)

stamina_system = StaminaSystem(800, 600, 1000, 300, 5, display_mode="both")

game_objects = GameObjects(
    SCREEN_WIDTH, SCREEN_HEIGHT, player_paddle, ball, stamina_system, opponent_paddle
)

PLAYER_SCORE = 0
OPPONENT_SCORE = 0
WINNING_SCORE = 10

PLAYER_SCORE, OPPONENT_SCORE = ball.move_ball(
    player_paddle.rect, opponent_paddle.rect, PLAYER_SCORE, OPPONENT_SCORE
)

while PLAYER_SCORE < WINNING_SCORE and OPPONENT_SCORE < WINNING_SCORE:
    clock.tick(FPS)
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        stamina_system.update_stamina(event, keys)

    PLAYER_BOOST_ACTIVE = stamina_system.boost_active
    OPPONENT_BOOST_ACTIVE = stamina_system.right_boost_active

    player_paddle.move_paddle(keys, not PLAYER_BOOST_ACTIVE)
    opponent_paddle.move_paddle(keys, not OPPONENT_BOOST_ACTIVE, True)
    PLAYER_SCORE, OPPONENT_SCORE = ball.move_ball(
        player_paddle.rect, opponent_paddle.rect, PLAYER_SCORE, OPPONENT_SCORE
    )

    game_objects.draw(screen, PLAYER_SCORE, OPPONENT_SCORE, stamina_system)
    pygame.display.flip()

screen.fill((0, 0, 0))
MESSAGE = "Player 1 win!" if PLAYER_SCORE > OPPONENT_SCORE else "Player 2 win!"
message_text = font.render(MESSAGE, True, FONT_COLOR)
screen.blit(
    message_text,
    (
        SCREEN_WIDTH // 2 - message_text.get_SCREEN_width() // 2,
        SCREEN_HEIGHT // 2 - message_text.get_SCREEN_height() // 2,
    ),
)
pygame.display.flip()

pygame.time.delay(3000)
pygame.quit()
sys.exit()
