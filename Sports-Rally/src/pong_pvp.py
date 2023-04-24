import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

FPS = 60
clock = pygame.time.Clock()

# Crucial values
paddle_width, paddle_height = 20, 100
player_speed_normal = 5
player_speed_boosted = 15
opponent_speed_normal = 5
opponent_speed_boosted = 15
player_paddle = pygame.Rect(
    100, HEIGHT // 2 - paddle_height // 2, paddle_width, paddle_height)
opponent_paddle = pygame.Rect(
    WIDTH - 130, HEIGHT // 2 - paddle_height // 2, paddle_width, paddle_height)

ball_size = 20
ball_speed = 4
ball = pygame.Rect(WIDTH // 2 - ball_size // 2, HEIGHT //
                   2 - ball_size // 2, ball_size, ball_size)
ball_dx, ball_dy = ball_speed, ball_speed

# Stamina system. The player starts with a stamina value of 0.
# When the player's speed is not boosted, a stamina value is added every 2.5 seconds.
# The stamina value is displayed as blocks in the lower left corner of the screen.
# When the left shift key is pressed, the stamina recharge is paused, and each second of speed boost consumes one block from the stamina stack.
# Constants for the stamina system
STAMINA_RECHARGE_TIME = 3000
STAMINA_CONSUME_TIME = 250
MAX_STAMINA_BLOCKS = 5
STAMINA_RECHARGE_EVENT = pygame.USEREVENT + 1
STAMINA_CONSUME_EVENT = pygame.USEREVENT + 2

# Initialize the stamina timers
pygame.time.set_timer(STAMINA_RECHARGE_EVENT, STAMINA_RECHARGE_TIME)
pygame.time.set_timer(STAMINA_CONSUME_EVENT, STAMINA_CONSUME_TIME)

# Variables for the stamina system
stamina_blocks = 0
stamina_recharge_timer = 0
stamina_consume_timer = 0
boost_active = False

# Variables for the right player's stamina system
right_stamina_blocks = 0
right_stamina_recharge_timer = 0
right_stamina_consume_timer = 0
right_boost_active = False

player_score = 0
opponent_score = 0
winning_score = 10
font = pygame.font.Font(None, 36)

# Stamina handling
def handle_stamina(keys, stamina_blocks, stamina_recharge_timer, stamina_consume_timer, boost_key, prev_key_state):
    boost_active = False

    if keys[boost_key] and stamina_blocks > 0:
        boost_active = True

        if stamina_recharge_timer > 0:
            stamina_recharge_timer = 0
    else:
        if prev_key_state and stamina_blocks > 0:
            stamina_blocks = max(0, stamina_blocks - 1)  # Consume only 1 block when the shift key is released

    return boost_active, stamina_blocks, stamina_recharge_timer, stamina_consume_timer, keys[boost_key]


# Displaying stamina for both players
def draw_stamina():
    block_width, block_height = 20, 10
    block_gap = 2

    # Left player's stamina blocks
    for i in range(stamina_blocks):
        block_x = 10
        block_y = HEIGHT - (i + 1) * (block_height + block_gap)
        pygame.draw.rect(screen, WHITE, (block_x, block_y,
                         block_width, block_height))

    # Right player's stamina blocks
    for i in range(right_stamina_blocks):
        block_x = WIDTH - 10 - block_width
        block_y = HEIGHT - (i + 1) * (block_height + block_gap)
        pygame.draw.rect(screen, WHITE, (block_x, block_y,
                         block_width, block_height))

# Paddle movement
def move_paddles():
    global player_speed_normal, player_speed_boosted, opponent_speed_normal, opponent_speed_boosted
    keys = pygame.key.get_pressed()

    player_speed = player_speed_boosted if keys[pygame.K_LSHIFT] and boost_active else player_speed_normal
    right_player_speed = opponent_speed_boosted if keys[pygame.K_RSHIFT] and right_boost_active else opponent_speed_normal

    if keys[pygame.K_w] and player_paddle.top > 0:
        player_paddle.y -= player_speed
    if keys[pygame.K_s] and player_paddle.bottom < HEIGHT:
        player_paddle.y += player_speed

    if keys[pygame.K_UP] and opponent_paddle.top > 0:
        opponent_paddle.y -= right_player_speed
    if keys[pygame.K_DOWN] and opponent_paddle.bottom < HEIGHT:
        opponent_paddle.y += right_player_speed


def calculate_opponent_target_y(ball_y, paddle_height, ball_height):
    return ball_y - (paddle_height - ball_height) // 2

def adjust_opponent_paddle_y(paddle_y, target_y, speed):
    if paddle_y < target_y:
        return paddle_y + min(speed, target_y - paddle_y)
    elif paddle_y > target_y:
        return paddle_y - min(speed, paddle_y - target_y)
    return paddle_y

# Reseting ball after point is granted
def reset_ball(granter):
    global ball, ball_dx, ball_dy, ball_speed
    ball = pygame.Rect(WIDTH // 2 - ball_size // 2, HEIGHT //
                       2 - ball_size // 2, ball_size, ball_size)
    ball_dx, ball_dy = ball_speed, ball_speed

    if granter == "opponent":
        ball_dx = ball_speed 
    elif granter == "player":
        ball_dx = -ball_speed 

# Ball movement
def move_ball():
    global ball_dx, ball_dy, player_score, opponent_score
    ball.x += ball_dx
    ball.y += ball_dy

    if ball.left <= 0:
        ball_dx = ball_speed
        opponent_score += 1
        reset_ball("opponent")
    elif ball.right >= WIDTH:
        ball_dx = -ball_speed
        player_score += 1
        reset_ball("player")
    elif ball.colliderect(player_paddle) and ball_dx < 0:
        ball_dx = ball_speed
    elif ball.colliderect(opponent_paddle) and ball_dx > 0:
        ball_dx = -ball_speed
    if ball.top <= 0 or ball.bottom >= HEIGHT:
        ball_dy *= -1

# Displaying game objects
def draw_objects():
    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, WHITE, player_paddle)
    pygame.draw.rect(screen, WHITE, opponent_paddle)
    pygame.draw.ellipse(screen, WHITE, ball)
    pygame.draw.aaline(screen, WHITE, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT))

    score_text = font.render(f"{player_score} - {opponent_score}", True, WHITE)
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 10))

    draw_stamina()

prev_left_shift_state = False
prev_right_shift_state = False
# Game loop
while player_score < winning_score and opponent_score < winning_score:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == STAMINA_RECHARGE_EVENT:
            if stamina_blocks < MAX_STAMINA_BLOCKS and not boost_active:
                stamina_blocks += 1
            if right_stamina_blocks < MAX_STAMINA_BLOCKS and not right_boost_active:
                right_stamina_blocks += 1
        elif event.type == STAMINA_CONSUME_EVENT:
            if boost_active:
                stamina_blocks = max(0, stamina_blocks - 1)
            if right_boost_active:
                right_stamina_blocks = max(0, right_stamina_blocks - 1)
    boost_active, stamina_blocks, stamina_recharge_timer, stamina_consume_timer, prev_left_shift_state = handle_stamina(
        pygame.key.get_pressed(),
        stamina_blocks,
        stamina_recharge_timer,
        stamina_consume_timer,
        pygame.K_LSHIFT,
        prev_left_shift_state,
    )
    right_boost_active, right_stamina_blocks, right_stamina_recharge_timer, right_stamina_consume_timer, prev_right_shift_state = handle_stamina(
        pygame.key.get_pressed(),
        right_stamina_blocks,
        right_stamina_recharge_timer,
        right_stamina_consume_timer,
        pygame.K_RSHIFT,
        prev_right_shift_state,
    )
    move_paddles()
    move_ball()
    draw_objects()
    draw_stamina()

    pygame.display.flip()

screen.fill((0, 0, 0))  # Clear the screen before displaying the message
message = "Player 1 win!" if player_score > opponent_score else "Player 2 win!"
message_text = font.render(message, True, WHITE)
screen.blit(message_text, (WIDTH // 2 - message_text.get_width() //
            2, HEIGHT // 2 - message_text.get_height() // 2))
pygame.display.flip()

# Adds a delay before quitting the game
pygame.time.delay(3000)
pygame.quit()
sys.exit()
