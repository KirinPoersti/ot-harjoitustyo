import unittest
from unittest.mock import MagicMock, Mock, patch
import pygame
from ..classes.pong_class import Paddle, Ball, StaminaSystem, GameObjects

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FONT_COLOR = (255, 255, 255)
FPS = 60


class TestPaddle(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.screen = pygame.display.set_mode((640, 480))
        self.paddle = Paddle(50, 50, 10, 50, 500)

    def test_init(self):
        self.assertEqual(self.paddle.rect.x, 50)
        self.assertEqual(self.paddle.rect.y, 50)
        self.assertEqual(self.paddle.rect.width, 10)
        self.assertEqual(self.paddle.rect.height, 50)
        self.assertEqual(self.paddle.screen_height, 500)

    def test_move_paddle_up(self):
        keys = {
            pygame.K_w: True,
            pygame.K_s: False,
            pygame.K_UP: False,
            pygame.K_DOWN: False,
            pygame.K_LSHIFT: False,
            pygame.K_RSHIFT: False,
        }
        new_y = self.paddle.move_paddle(keys, False)
        self.assertEqual(new_y, 45)

    def test_move_paddle_down(self):
        keys = {
            pygame.K_w: False,
            pygame.K_s: True,
            pygame.K_UP: False,
            pygame.K_DOWN: False,
            pygame.K_LSHIFT: False,
            pygame.K_RSHIFT: False,
        }
        new_y = self.paddle.move_paddle(keys, False)
        self.assertEqual(new_y, 55)

    def test_move_paddle_up_boosted(self):
        keys = {
            pygame.K_w: True,
            pygame.K_s: False,
            pygame.K_UP: False,
            pygame.K_DOWN: False,
            pygame.K_LSHIFT: True,
            pygame.K_RSHIFT: False,
        }
        new_y = self.paddle.move_paddle(keys, True)
        self.assertEqual(new_y, 35)

    def test_move_paddle_down_boosted(self):
        keys = {
            pygame.K_w: False,
            pygame.K_s: True,
            pygame.K_UP: False,
            pygame.K_DOWN: False,
            pygame.K_LSHIFT: True,
            pygame.K_RSHIFT: False,
        }
        new_y = self.paddle.move_paddle(keys, True)
        self.assertEqual(new_y, 65)

    def test_move_paddle_opponent_up(self):
        keys = {
            pygame.K_w: False,
            pygame.K_s: False,
            pygame.K_UP: True,
            pygame.K_DOWN: False,
            pygame.K_LSHIFT: False,
            pygame.K_RSHIFT: True,
        }
        new_y = self.paddle.move_paddle(keys, True, is_opponent=True)
        self.assertEqual(new_y, 35)

    def test_move_paddle_opponent_down(self):
        keys = {
            pygame.K_w: False,
            pygame.K_s: False,
            pygame.K_UP: False,
            pygame.K_DOWN: True,
            pygame.K_LSHIFT: False,
            pygame.K_RSHIFT: True,
        }
        new_y = self.paddle.move_paddle(keys, True, is_opponent=True)
        self.assertEqual(new_y, 65)

    def test_draw_paddle(self):
        result = self.paddle.draw(self.screen)
        self.assertEqual(result, "Object drawn")


class TestBall(unittest.TestCase):
    def setUp(self):
        self.sound_manager = Mock()
        self.ball = Ball(800, 600, 15, 5, self.sound_manager,
                         practice_mode=True)
        self.player_paddle = Mock()
        self.opponent_paddle = Mock()

    def test_reset_ball_practice(self):
        self.ball.reset_ball_practice()
        self.assertEqual(
            self.ball.ball.x, self.ball.width // 2 - self.ball.ball_radius // 2
        )
        self.assertEqual(
            self.ball.ball.y, self.ball.height // 2 - self.ball.ball_radius // 2
        )

    def test_reset_ball_pvp_player_granter(self):
        self.ball.reset_ball_pvp("player")
        self.assertEqual(
            self.ball.ball.x, self.ball.width // 2 - self.ball.ball_radius // 2
        )
        self.assertEqual(
            self.ball.ball.y, self.ball.height // 2 - self.ball.ball_radius // 2
        )

    def test_reset_ball_pvp_opponent_granter(self):
        self.ball.reset_ball_pvp("opponent")
        self.assertEqual(
            self.ball.ball.x, self.ball.width // 2 - self.ball.ball_radius // 2
        )
        self.assertEqual(
            self.ball.ball.y, self.ball.height // 2 - self.ball.ball_radius // 2
        )

    def test_practice_mode_true(self):
        self.sound_manager = Mock()
        self.ball = Ball(800, 600, 15, 5, self.sound_manager,
                         practice_mode=True)
        self.assertEqual(self.ball.ball_dx, -5)
        self.assertEqual(self.ball.ball_dy, 5)

    def test_practice_mode_false(self):
        self.sound_manager = Mock()
        self.ball = Ball(800, 600, 15, 5, self.sound_manager,
                         practice_mode=False)
        self.assertEqual(self.ball.ball_dx, 5)
        self.assertEqual(self.ball.ball_dy, 5)


class TestStaminaSystem(unittest.TestCase):
    def setUp(self):
        self.system = StaminaSystem(
            width=800,
            height=600,
            stamina_recharge_time=1000,
            stamina_consume_time=1000,
            max_stamina_blocks=10,
            display_mode="both",
        )

    @patch("pygame.time.set_timer")
    def test_init(self, mock_set_timer):
        system = StaminaSystem(
            width=800,
            height=600,
            stamina_recharge_time=1000,
            stamina_consume_time=300,
            max_stamina_blocks=5,
            display_mode="both",
        )

        self.assertEqual(system.width, 800)
        self.assertEqual(system.height, 600)
        self.assertEqual(system.stamina_recharge_time, 1000)
        self.assertEqual(system.stamina_consume_time, 300)
        self.assertEqual(system.max_stamina_blocks, 5)
        self.assertEqual(system.display_mode, "both")

        self.assertEqual(system.stamina_blocks, 0)
        self.assertEqual(system.stamina_recharge_timer, 0)
        self.assertEqual(system.stamina_consume_timer, 0)
        self.assertEqual(system.boost_active, False)

        self.assertEqual(system.right_stamina_blocks, 0)
        self.assertEqual(system.right_stamina_recharge_timer, 0)
        self.assertEqual(system.right_stamina_consume_timer, 0)
        self.assertEqual(system.right_boost_active, False)

        self.assertEqual(system.prev_left_shift_state, False)
        self.assertEqual(system.prev_right_shift_state, False)

        mock_set_timer.assert_any_call(pygame.USEREVENT + 1, 1000)
        mock_set_timer.assert_any_call(pygame.USEREVENT + 2, 300)

    @patch("pygame.draw.rect")
    def test_draw_stamina(self, mock_rect):
        screen = Mock()
        self.system.stamina_blocks = 5
        self.system.right_stamina_blocks = 5
        self.system.draw_stamina(screen)
        self.assertEqual(mock_rect.call_count, 10)

    def test_update_stamina(self):
        event = Mock()
        keys = {pygame.K_LSHIFT: False, pygame.K_RSHIFT: False}
        event.type = pygame.USEREVENT + 1
        self.system.update_stamina(event, keys)
        self.assertEqual(self.system.stamina_blocks, 1)
        self.assertEqual(self.system.right_stamina_blocks, 1)

        event.type = pygame.USEREVENT + 2
        self.system.update_stamina(event, keys)
        self.assertEqual(self.system.stamina_blocks, 1)
        self.assertEqual(self.system.right_stamina_blocks, 1)

        keys = {pygame.K_LSHIFT: True, pygame.K_RSHIFT: True}
        self.system.boost_active = True
        self.system.right_boost_active = True
        self.system.update_stamina(event, keys)
        self.assertEqual(self.system.stamina_blocks, 0)
        self.assertEqual(self.system.right_stamina_blocks, 0)

    def test_handle_stamina_boost_active(self):
        keys = {pygame.K_LSHIFT: True}
        results = self.system.handle_stamina(
            keys,
            stamina_blocks=1,
            stamina_recharge_timer=1,
            stamina_consume_timer=1,
            boost_key=pygame.K_LSHIFT,
            prev_key_state=False,
            is_opponent=False,
        )
        self.assertEqual(results, (True, 1, 0, 1, True))

    def test_handle_stamina_boost_not_active(self):
        keys = {pygame.K_LSHIFT: False}
        results = self.system.handle_stamina(
            keys,
            stamina_blocks=1,
            stamina_recharge_timer=1,
            stamina_consume_timer=1,
            boost_key=pygame.K_LSHIFT,
            prev_key_state=True,
            is_opponent=False,
        )
        self.assertEqual(results, (False, 0, 1, 1, False))

    def test_handle_stamina_is_opponent(self):
        keys = {pygame.K_LSHIFT: True}
        results = self.system.handle_stamina(
            keys,
            stamina_blocks=1,
            stamina_recharge_timer=1,
            stamina_consume_timer=1,
            boost_key=pygame.K_LSHIFT,
            prev_key_state=False,
            is_opponent=True,
        )
        self.assertEqual(results, (False, 1, 1, 1, True))

    def test_handle_stamina_when_stamina_recharge_timer_is_not_zero(self):
        keys = {pygame.K_LSHIFT: False}
        stamina_blocks = 1
        stamina_recharge_timer = 0
        stamina_consume_timer = 0
        boost_key = pygame.K_LSHIFT
        prev_key_state = False
        is_opponent = False

        (
            boost_active,
            stamina_blocks,
            stamina_recharge_timer,
            stamina_consume_timer,
            prev_key_state,
        ) = self.system.handle_stamina(
            keys,
            stamina_blocks,
            stamina_recharge_timer,
            stamina_consume_timer,
            boost_key,
            prev_key_state,
            is_opponent,
        )

        self.assertFalse(boost_active)
        self.assertEqual(stamina_blocks, 1)
        self.assertEqual(stamina_recharge_timer, 0)
        self.assertEqual(stamina_consume_timer, 0)
        self.assertFalse(prev_key_state)


class TestGameObjects(unittest.TestCase):
    def setUp(self):
        self.mock_paddle = Mock()
        self.mock_ball = Mock()
        self.mock_stamina_system = Mock()
        self.mock_opponent_paddle = Mock()
        self.mock_screen = Mock()

    @patch("pygame.font.Font")
    def test_init(self, mock_font):
        game_objects = GameObjects(
            width=800,
            height=600,
            player_paddle=self.mock_paddle,
            ball=self.mock_ball,
            stamina_system=self.mock_stamina_system,
            opponent_paddle=self.mock_opponent_paddle,
            practice_mode=False,
        )

        self.assertEqual(game_objects.width, 800)
        self.assertEqual(game_objects.height, 600)
        self.assertEqual(game_objects.player_paddle, self.mock_paddle)
        self.assertEqual(game_objects.ball, self.mock_ball)
        self.assertEqual(game_objects.stamina_system, self.mock_stamina_system)
        self.assertEqual(game_objects.opponent_paddle,
                         self.mock_opponent_paddle)
        self.assertEqual(game_objects.practice_mode, False)
        mock_font.assert_called_once_with(None, 50)

    @patch("pygame.draw")
    def test_draw(self, mock_draw):
        game_objects = GameObjects(
            width=800,
            height=600,
            player_paddle=self.mock_paddle,
            ball=self.mock_ball,
            stamina_system=self.mock_stamina_system,
            opponent_paddle=self.mock_opponent_paddle,
            practice_mode=False,
        )

        mock_screen = Mock()
        game_objects.draw(mock_screen, 1, 2, self.mock_stamina_system)

        self.mock_paddle.draw.assert_called_once_with(mock_screen)
        self.mock_opponent_paddle.draw.assert_called_once_with(mock_screen)
        mock_draw.ellipse.assert_called_once_with(
            mock_screen, FONT_COLOR, self.mock_ball.ball
        )
        self.mock_stamina_system.draw_stamina.assert_called_once_with(
            mock_screen)
        mock_draw.rect.assert_called()

    @patch("pygame.draw.line")
    @patch("pygame.draw.ellipse")
    @patch("pygame.draw.rect")
    def test_draw_practice(self, mock_draw_rect, mock_draw_ellipse, mock_draw_line):
        game_objects = GameObjects(
            width=800,
            height=600,
            player_paddle=self.mock_paddle,
            ball=self.mock_ball,
            stamina_system=self.mock_stamina_system,
            opponent_paddle=self.mock_opponent_paddle,
            practice_mode=True,
        )

        game_objects.draw_practice(
            self.mock_screen, 1, self.mock_stamina_system)

        self.mock_screen.fill.assert_called_once_with((0, 0, 0))
        self.mock_paddle.draw.assert_called_once_with(self.mock_screen)
        if self.mock_opponent_paddle is not None:
            self.mock_opponent_paddle.draw.assert_called_once_with(
                self.mock_screen)
        mock_draw_ellipse.assert_called()
        self.mock_screen.blit.assert_called()
        self.mock_stamina_system.draw_stamina.assert_called_once_with(
            self.mock_screen)
        mock_draw_rect.assert_called()


class TestIntegration(unittest.TestCase):
    def setUp(self):
        self.screen_height = 600
        self.screen = pygame.Surface((800, 600))
        self.paddle = Paddle(100, 100, 10, 100, self.screen_height)
        self.sound_manager = MagicMock()
        self.ball = Ball(100, 100, 10, 5, self.sound_manager)
        self.stamina_system = StaminaSystem(800, 600, 1000, 500, 10)
        self.opponent_paddle = Paddle(300, 300, 10, 100, self.screen_height)
        self.game_objects = GameObjects(
            800, 600, self.paddle, self.ball, self.stamina_system, self.opponent_paddle
        )

    @patch("pygame.draw.rect")
    def test_paddle_and_ball(self, mock_rect):
        keys = {
            pygame.K_LSHIFT: False,
            pygame.K_w: True,
            pygame.K_s: False,
            pygame.K_RSHIFT: False,
            pygame.K_UP: False,
            pygame.K_DOWN: False,
        }
        self.paddle.move_paddle(keys, False)
        self.assertEqual(self.paddle.rect.y, 95)

        self.ball.move_ball(self.paddle, self.opponent_paddle, 0, 0)
        self.assertEqual(self.ball.ball.x, 50)
        self.assertEqual(self.ball.ball.y, 50)

        self.paddle.draw(self.screen)
        mock_rect.assert_called_once()

    @patch("pygame.draw.rect")
    def test_game_objects_draw_practice(self, mock_rect):
        self.game_objects.draw_practice(self.screen, 10, self.stamina_system)
        mock_rect.assert_called()

    @patch("pygame.draw.rect")
    def test_game_objects_draw(self, mock_rect):
        self.game_objects.draw(self.screen, 10, 10, self.stamina_system)
        mock_rect.assert_called()


if __name__ == "__main__":
    unittest.main()
