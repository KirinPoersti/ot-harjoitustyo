import random
import math
import pygame

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FONT_COLOR = (255, 255, 255)
FPS = 60


class Paddle:
    """
    This class represents a paddle in the game.

    Attributes:
        rect: A pygame rectangle representing the paddle.
        speed_normal: The normal speed of the paddle.
        speed_boosted: The boosted speed of the paddle.
        screen_height: The height of the screen.
    """

    def __init__(self, paddle_x, paddle_y, width, height, screen_height):
        """Initialize the Paddle class with position, size and screen height."""
        self.rect = pygame.Rect(paddle_x, paddle_y, width, height)
        self.speed_normal = 5
        self.speed_boosted = 15
        self.screen_height = screen_height

    def move_paddle(self, keys, boost_active, is_opponent=False):
        """
        Moves the paddle based on the keys pressed.
        If 'w' or 'UP' is pressed, the paddle moves up.
        If 's' or 'DOWN' is pressed, the paddle moves down.
        """
        speed = (
            self.speed_boosted
            if (keys[pygame.K_LSHIFT] and not is_opponent)
            or (keys[pygame.K_RSHIFT] and is_opponent)
            and boost_active
            else self.speed_normal
        )
        if keys[pygame.K_w] and self.rect.top > 0 and not is_opponent:
            self.rect.y -= speed
        if (
            keys[pygame.K_s]
            and self.rect.bottom < self.screen_height
            and not is_opponent
        ):
            self.rect.y += speed

        if keys[pygame.K_UP] and self.rect.top > 0 and is_opponent:
            self.rect.y -= speed
        if (
            keys[pygame.K_DOWN]
            and self.rect.bottom < self.screen_height
            and is_opponent
        ):
            self.rect.y += speed
        return self.rect.y

    def draw(self, screen):
        """Draws the paddle on the screen."""
        pygame.draw.rect(screen, FONT_COLOR, self.rect)
        return "Object drawn"


class Ball:
    """
    This class represents a ball in the game.

    Attributes:
        width: Width of the screen.
        height: Height of the screen.
        ball_radius: Radius of the ball.
        speed: Speed of the ball.
        sound_manager: Manager for the game's sound effects.
        practice_mode: Boolean indicating whether the game is in practice mode.
    """

    def __init__(
        self, width, height, ball_radius, speed, sound_manager, practice_mode=False
    ):
        """Initialize the Ball class with its attributes."""
        self.width = width
        self.height = height
        self.ball_radius = ball_radius
        self.speed = speed
        self.sound_manager = sound_manager
        self.practice_mode = practice_mode

        self.ball = pygame.Rect(
            width // 2 - ball_radius // 2,
            height // 2 - ball_radius // 2,
            ball_radius,
            ball_radius,
        )
        if self.practice_mode:
            self.ball_dx, self.ball_dy = -speed, speed
        else:
            self.ball_dx, self.ball_dy = speed, speed

    def reset_ball_practice(self):
        """Resets the ball's position and direction in practice mode."""
        self.ball.x = self.width // 2 - self.ball_radius // 2
        self.ball.y = self.height // 2 - self.ball_radius // 2
        angle = random.uniform(math.radians(315), math.radians(405))
        self.ball_dx = -abs(self.speed) * math.cos(angle)
        self.ball_dy = self.speed * math.sin(angle)
        return "Ball reset"

    def reset_ball_pvp(self, granter=None):
        """Resets the ball's position and direction in player versus player mode."""
        self.ball.x = self.width // 2 - self.ball_radius // 2
        self.ball.y = self.height // 2 - self.ball_radius // 2
        self.ball_dx = -abs(self.speed) if granter == "player" else abs(self.speed)
        self.ball_dy = self.speed
        return "Ball reset"

    def move_ball_practice(
        self, player_paddle, player_score, opponent_score, opponent_paddle=None
    ):
        """Moves the ball in practice mode and updates the scores based on collisions."""
        self.ball.x += self.ball_dx
        self.ball.y += self.ball_dy

        if self.ball.colliderect(player_paddle) and self.ball_dx < 0:
            print("Player paddle collision")
            self.sound_manager.play_paddle_sound()
            self.ball_dx = abs(self.speed)
            player_score += 1
            self.reset_ball_practice()
        # even tho opponent paddle does not exist in practice mode
        # but I've noticed that if the exact parameter does not exist,
        # it would create errors causing the game to either not launch at all or just crash
        # hence keeping the following if loop is just to make sure that the game runs with ease
        if (
            opponent_paddle is not None
            and self.ball.colliderect(opponent_paddle)
            and self.ball_dx > 0
        ):
            print("Opponent paddle collision")
            self.sound_manager.play_paddle_sound()
            self.ball_dx = -abs(self.speed)
            opponent_score += 1
            self.reset_ball_practice()

        if self.ball.top <= 0 or self.ball.bottom >= self.height:
            print("Wall collision")
            self.sound_manager.play_wall_sound()
            self.ball_dy *= -1

        if self.ball.left <= 0 or self.ball.right >= self.width:
            print("Out of bounds")
            self.reset_ball_practice()

        return player_score, opponent_score

    def move_ball(self, player_paddle, opponent_paddle, player_score, opponent_score):
        """Moves the ball in player versus player mode and updates the scores based on collisions."""
        self.ball.x += self.ball_dx
        self.ball.y += self.ball_dy

        if self.ball.left <= 0:
            self.ball_dx = self.speed
            opponent_score += 1
            self.reset_ball_pvp("opponent")
        elif self.ball.right >= self.width:
            self.ball_dx = -self.speed
            player_score += 1
            self.reset_ball_pvp("player")
        elif self.ball.colliderect(player_paddle) and self.ball_dx < 0:
            self.ball_dx = self.speed
            self.sound_manager.play_paddle_sound()
        elif self.ball.colliderect(opponent_paddle) and self.ball_dx > 0:
            self.ball_dx = -self.speed
            self.sound_manager.play_paddle_sound()

        if self.ball.top <= 0 or self.ball.bottom >= self.height:
            self.ball_dy *= -1
            self.sound_manager.play_wall_sound()

        return player_score, opponent_score


class StaminaSystem:
    """
    This class represents a StaminaSystem in the game.

    Attributes:
        width: Width of the screen.
        height: Height of the screen.
        stamina_recharge_time: Time for the stamina to recharge.
        stamina_consume_time: Time for the stamina to be consumed.
        max_stamina_blocks: Maximum number of stamina blocks.
        display_mode: Mode of display for the stamina.
    """

    def __init__(
        self,
        width,
        height,
        stamina_recharge_time,
        stamina_consume_time,
        max_stamina_blocks,
        display_mode="both",
    ):
        """Initialize the StaminaSystem class with its attributes."""
        self.width = width
        self.height = height
        self.stamina_recharge_time = stamina_recharge_time
        self.stamina_consume_time = stamina_consume_time
        self.max_stamina_blocks = max_stamina_blocks
        self.display_mode = display_mode

        self.stamina_blocks = 0
        self.stamina_recharge_timer = 0
        self.stamina_consume_timer = 0
        self.boost_active = False

        self.right_stamina_blocks = 0
        self.right_stamina_recharge_timer = 0
        self.right_stamina_consume_timer = 0
        self.right_boost_active = False

        self.prev_left_shift_state = False
        self.prev_right_shift_state = False

        pygame.time.set_timer(pygame.USEREVENT + 1, self.stamina_recharge_time)
        pygame.time.set_timer(pygame.USEREVENT + 2, self.stamina_consume_time)

    def handle_stamina(
        self,
        keys,
        stamina_blocks,
        stamina_recharge_timer,
        stamina_consume_timer,
        boost_key,
        prev_key_state,
        is_opponent,
    ):
        """
        Handles the stamina system based on the keys pressed and
        the current state of the stamina blocks and timers.
        """
        boost_active = False

        if keys[boost_key] and stamina_blocks > 0 and not is_opponent:
            boost_active = True

            if stamina_recharge_timer > 0:
                stamina_recharge_timer = 0
        else:
            if prev_key_state and stamina_blocks > 0:
                stamina_blocks = max(0, stamina_blocks - 1)

        return (
            boost_active,
            stamina_blocks,
            stamina_recharge_timer,
            stamina_consume_timer,
            keys[boost_key],
        )

    def draw_stamina(self, screen):
        """Draws the stamina blocks on the screen."""
        block_width, block_height = 20, 10
        block_gap = 2
        if self.display_mode in ["left", "both"]:
            for i in range(self.stamina_blocks):
                block_x = 10
                block_y = self.height - (i + 1) * (block_height + block_gap)
                pygame.draw.rect(
                    screen,
                    (255, 255, 255),
                    (block_x, block_y, block_width, block_height),
                )
        if self.display_mode == "both":
            for i in range(self.right_stamina_blocks):
                block_x = self.width - 10 - block_width
                block_y = self.height - (i + 1) * (block_height + block_gap)
                pygame.draw.rect(
                    screen,
                    (255, 255, 255),
                    (block_x, block_y, block_width, block_height),
                )

    def update_stamina(self, event, keys):
        """Updates the stamina blocks and timers based on events and keys pressed."""
        if event.type == pygame.USEREVENT + 1:
            if self.stamina_blocks < self.max_stamina_blocks and not self.boost_active:
                self.stamina_blocks += 1
            if (
                self.right_stamina_blocks < self.max_stamina_blocks
                and not self.right_boost_active
            ):
                self.right_stamina_blocks += 1
        elif event.type == pygame.USEREVENT + 2:
            if self.boost_active:
                self.stamina_blocks = max(0, self.stamina_blocks - 1)
            if self.right_boost_active:
                self.right_stamina_blocks = max(0, self.right_stamina_blocks - 1)

            (
                self.boost_active,
                self.stamina_blocks,
                self.stamina_recharge_timer,
                self.stamina_consume_timer,
                self.prev_left_shift_state,
            ) = self.handle_stamina(
                keys,
                self.stamina_blocks,
                self.stamina_recharge_timer,
                self.stamina_consume_timer,
                pygame.K_LSHIFT,
                self.prev_left_shift_state,
                False,
            )
            (
                self.right_boost_active,
                self.right_stamina_blocks,
                self.right_stamina_recharge_timer,
                self.right_stamina_consume_timer,
                self.prev_right_shift_state,
            ) = self.handle_stamina(
                keys,
                self.right_stamina_blocks,
                self.right_stamina_recharge_timer,
                self.right_stamina_consume_timer,
                pygame.K_RSHIFT,
                self.prev_right_shift_state,
                True,
            )


class GameObjects:
    """Main class that controls all the game objects including the paddles, ball, and stamina system.

    Attributes:
        width (int): Width of the game screen.
        height (int): Height of the game screen.
        player_paddle (Paddle): Paddle object for the player.
        ball (Ball): Ball object for the game.
        stamina_system (StaminaSystem): Stamina system object for the game.
        opponent_paddle (Paddle): Paddle object for the opponent.
        practice_mode (bool): Flag to indicate whether the game is in practice mode or not.
        font (pygame.font.Font): Font object for rendering text in the game.
    """

    def __init__(
        self,
        width,
        height,
        player_paddle,
        ball,
        stamina_system,
        opponent_paddle=None,
        practice_mode=False,
    ):
        self.width = width
        self.height = height
        self.player_paddle = player_paddle
        self.ball = ball
        self.stamina_system = stamina_system
        self.opponent_paddle = opponent_paddle
        self.practice_mode = practice_mode

        self.font = pygame.font.Font(None, 50)

    def draw_practice(self, screen, player_score, stamina_system):
        """Draws all game objects during practice mode.

        Args:
            screen (pygame.Surface): Pygame screen surface.
            player_score (int): Current score of the player.
            stamina_system (StaminaSystem): Stamina system object for the game.
        """
        screen.fill((0, 0, 0))
        self.player_paddle.draw(screen)
        if self.opponent_paddle is not None:
            self.opponent_paddle.draw(screen)
        pygame.draw.ellipse(screen, FONT_COLOR, self.ball.ball)
        for y in range(0, SCREEN_HEIGHT, 40):
            pygame.draw.rect(screen, FONT_COLOR, (SCREEN_WIDTH // 2 - 2, y + 40, 4, 20))
        score_text = self.font.render(f"Score: {player_score}", True, FONT_COLOR)
        screen.blit(score_text, (self.width // 2 - score_text.get_width() // 2, 10))

        stamina_system.draw_stamina(screen)

    def draw(self, screen, player_score, opponent_score, stamina_system):
        """Draws all game objects during normal game mode.

        Args:
            screen (pygame.Surface): Pygame screen surface.
            player_score (int): Current score of the player.
            opponent_score (int): Current score of the opponent.
            stamina_system (StaminaSystem): Stamina system object for the game.
        """
        screen.fill((0, 0, 0))
        self.player_paddle.draw(screen)
        self.opponent_paddle.draw(screen)
        pygame.draw.ellipse(screen, FONT_COLOR, self.ball.ball)
        for y in range(0, SCREEN_HEIGHT, 40):
            pygame.draw.rect(screen, FONT_COLOR, (SCREEN_WIDTH // 2 - 2, y + 40, 4, 20))
        score_text = self.font.render(
            f"{player_score} - {opponent_score}", True, FONT_COLOR
        )
        screen.blit(score_text, (self.width // 2 - score_text.get_width() // 2, 10))
        stamina_system.draw_stamina(screen)
