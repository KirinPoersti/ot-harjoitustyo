import random
import math
import pygame

WHITE = (255, 255, 255)


class SoundManager:
    def __init__(self):
        pygame.mixer.init()
        self.paddle_sound = pygame.mixer.Sound("src/resources/pong_paddle.mp3")
        self.wall_sound = pygame.mixer.Sound("src/resources/pong_wall.mp3")
        self.pong_score_sound = pygame.mixer.Sound("src/resources/pong_score.mp3")
        self.boosted_sound = pygame.mixer.Sound("src/resources/pong_boosted.mp3")
        self.pong_bgm_sound = pygame.mixer.music.load("src/resources/pong_bgm.mp3")

        self.button_sound = pygame.mixer.Sound("src/resources/button.mp3")

        self.jump_sound = pygame.mixer.Sound("src/resources/longjump_jump.mp3")
        self.longjump_score_sound = pygame.mixer.Sound(
            "src/resources/longjump_score.mp3"
        )
        self.longjump_bgm_sound = pygame.mixer.music.load(
            "src/resources/longjump_bgm.mp3"
        )

    def play_paddle_sound(self):
        self.paddle_sound.play()

    def play_wall_sound(self):
        self.wall_sound.play()

    def play_pong_score_sound(self):
        self.pong_score_sound.play()

    def play_boosted_sound(self):
        self.boosted_sound.play()

    def play_pong_bgm_sound(self):
        self.pong_bgm_sound = pygame.mixer.music.load("src/resources/pong_bgm.mp3")
        pygame.mixer.music.set_volume(0.25)
        pygame.mixer.music.play(-1)

    def play_button_sound(self):
        self.button_sound.play()

    def play_jump_sound(self):
        self.jump_sound.play()

    def play_longjump_score_sound(self):
        self.longjump_score_sound.play()

    def play_longjump_bgm_sound(self):
        self.longjump_bgm_sound = pygame.mixer.music.load(
            "src/resources/longjump_bgm.mp3"
        )
        pygame.mixer.music.set_volume(0.25)
        pygame.mixer.music.play(-1)


class Paddle:
    def __init__(self, x, y, width, height, screen_height):
        self.rect = pygame.Rect(x, y, width, height)
        self.speed_normal = 5
        self.speed_boosted = 15
        self.screen_height = screen_height

    def move_paddle(self, keys, boost_active, is_opponent=False):
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

    def draw(self, screen):
        pygame.draw.rect(screen, WHITE, self.rect)


class Ball:
    def __init__(
        self, width, height, ball_radius, speed, sound_manager, practice_mode=False
    ):
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
            self.ball_dx, self.ball_dy = -speed, speed

    def reset_ball_practice(self):
        self.ball.x = self.width // 2 - self.ball_radius
        self.ball.y = self.height // 2 - self.ball_radius
        angle = random.uniform(math.radians(315), math.radians(405))
        self.ball_dx = -abs(self.speed) * math.cos(angle)
        self.ball_dy = self.speed * math.sin(angle)

    def reset_ball_pvp(self, granter=None):
        self.ball.x = self.width // 2 - self.ball_radius
        self.ball.y = self.height // 2 - self.ball_radius
        self.ball_dx = -abs(self.speed) if granter == "player" else abs(self.speed)
        self.ball_dy = self.speed

    def move_ball_practice(
        self, player_paddle, player_score, opponent_score, opponent_paddle=None
    ):
        self.ball.x += self.ball_dx
        self.ball.y += self.ball_dy

        if self.ball.colliderect(player_paddle) and self.ball_dx < 0:
            self.sound_manager.play_paddle_sound()
            self.ball_dx = abs(self.speed)
            player_score += 1
            self.reset_ball_practice()

        if (
            opponent_paddle is not None
            and self.ball.colliderect(opponent_paddle)
            and self.ball_dx > 0
        ):
            self.sound_manager.play_paddle_sound()
            self.ball_dx = -abs(self.speed)
            opponent_score += 1
            self.reset_ball_practice()

        if self.ball.top <= 0 or self.ball.bottom >= self.height:
            self.sound_manager.play_wall_sound()
            self.ball_dy *= -1

        if self.ball.left <= 0 or self.ball.right >= self.width:
            self.reset_ball_practice()

        return player_score, opponent_score

    def move_ball(self, player_paddle, opponent_paddle, player_score, opponent_score):
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
    def __init__(
        self,
        width,
        height,
        stamina_recharge_time,
        stamina_consume_time,
        max_stamina_blocks,
        display_mode="both",
    ):
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
        self.white = (255, 255, 255)

    def draw_practice(self, screen, player_score, stamina_system):
        screen.fill((0, 0, 0))
        self.player_paddle.draw(screen)
        if self.opponent_paddle is not None:
            self.opponent_paddle.draw(screen)
        pygame.draw.ellipse(screen, self.white, self.ball.ball)
        for y in range(0, 600, 40):
            pygame.draw.rect(screen, WHITE, (800 // 2 - 2, y + 40, 4, 20))
        score_text = self.font.render(f"Score: {player_score}", True, self.white)
        screen.blit(score_text, (self.width // 2 - score_text.get_width() // 2, 10))

        button_width, button_height = 40, 40
        exit_button = pygame.Rect(
            800 - button_width - 10, 10, button_width, button_height
        )
        pygame.draw.rect(screen, WHITE, exit_button, 3)
        pygame.draw.line(
            screen,
            WHITE,
            (exit_button.left + 10, exit_button.top + 10),
            (exit_button.right - 10, exit_button.bottom - 10),
            3,
        )
        pygame.draw.line(
            screen,
            WHITE,
            (exit_button.left + 10, exit_button.bottom - 10),
            (exit_button.right - 10, exit_button.top + 10),
            3,
        )
        stamina_system.draw_stamina(screen)

    def draw(self, screen, player_score, opponent_score, stamina_system):
        screen.fill((0, 0, 0))
        self.player_paddle.draw(screen)
        self.opponent_paddle.draw(screen)
        pygame.draw.ellipse(screen, self.white, self.ball.ball)
        for y in range(0, 600, 40):
            pygame.draw.rect(screen, WHITE, (800 // 2 - 2, y + 40, 4, 20))
        score_text = self.font.render(
            f"{player_score} - {opponent_score}", True, self.white
        )
        screen.blit(score_text, (self.width // 2 - score_text.get_width() // 2, 10))

        stamina_system.draw_stamina(screen)
