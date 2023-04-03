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
player_speed_boosted = 8
opponent_speed_normal = 5
opponent_speed_boosted = 8
player_paddle = pygame.Rect(100, HEIGHT // 2 - paddle_height // 2, paddle_width, paddle_height)
opponent_paddle = pygame.Rect(WIDTH - 130, HEIGHT // 2 - paddle_height // 2, paddle_width, paddle_height)

ball_size = 20
ball_speed = 4
ball = pygame.Rect(WIDTH // 2 - ball_size // 2, HEIGHT // 2 - ball_size // 2, ball_size, ball_size)
ball_dx, ball_dy = ball_speed, ball_speed

# Stamina system. The player starts with a stamina value of 0. 
# When the player's speed is not boosted, a stamina value is added every 2.5 seconds. 
# The stamina value is displayed as blocks in the lower left corner of the screen. 
# When the left shift key is pressed, the stamina recharge is paused, and each second of speed boost consumes one block from the stamina stack.
# Constants for the stamina system
STAMINA_RECHARGE_TIME = 2500
STAMINA_CONSUME_TIME = 1000
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

player_score = 0
opponent_score = 0
winning_score = 10
font = pygame.font.Font(None, 36)

# Updating stamina
def update_stamina():
    global stamina_blocks, boost_active, stamina_recharge_timer
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LSHIFT] and stamina_blocks > 0:
        boost_active = True
        if stamina_recharge_timer > 0:
            stamina_recharge_timer = 0
            pygame.time.set_timer(STAMINA_RECHARGE_EVENT, STAMINA_RECHARGE_TIME)
        if stamina_consume_timer == 0:
            stamina_blocks = max(0, stamina_blocks - 2) # changed from 1 to 2
            if stamina_blocks == 0:
                boost_active = False
                pygame.time.set_timer(STAMINA_CONSUME_EVENT, 0)
            else:
                pygame.time.set_timer(STAMINA_CONSUME_EVENT, STAMINA_CONSUME_TIME)
    else:
        boost_active = False
        if stamina_recharge_timer == 0:
            stamina_recharge_timer = pygame.time.get_ticks()
        else:
            if pygame.time.get_ticks() - stamina_recharge_timer > STAMINA_RECHARGE_TIME:
                stamina_blocks = min(stamina_blocks + 1, MAX_STAMINA_BLOCKS)
                stamina_recharge_timer = pygame.time.get_ticks()

# Displaying stamina
def draw_stamina():
    block_width, block_height = 20, 10
    block_gap = 5
    # Calculate the number of blocks to display based on the decimal value of stamina_blocks divided by MAX_STAMINA_BLOCKS
    num_blocks = int(stamina_blocks / MAX_STAMINA_BLOCKS * 5)
    for i in range(num_blocks):
        block_x = 10
        block_y = HEIGHT - (i + 1) * (block_height + block_gap)
        pygame.draw.rect(screen, WHITE, (block_x, block_y, block_width, block_height))


# Paddle movement
def move_paddles():
    global player_speed_normal, player_speed_boosted, opponent_speed_normal, opponent_speed_boosted
    keys = pygame.key.get_pressed()

    player_speed = player_speed_boosted if keys[pygame.K_LSHIFT] and boost_active else player_speed_normal

    if keys[pygame.K_UP] and player_paddle.top > 0:
        player_paddle.y -= player_speed
    if keys[pygame.K_DOWN] and player_paddle.bottom < HEIGHT:
        player_paddle.y += player_speed

    if ball_dx > 0:  # Opponent paddle moves only when the ball is moving towards it
        target_y = ball.y - (opponent_paddle.height - ball.height) // 2
        if opponent_paddle.y < target_y:
            opponent_paddle.y += min(opponent_speed_normal, target_y - opponent_paddle.y)
        elif opponent_paddle.y > target_y:
            opponent_paddle.y -= min(opponent_speed_normal, opponent_paddle.y - target_y)


def reset_paddles():
    global player_paddle, opponent_paddle
    player_paddle = pygame.Rect(100, HEIGHT // 2 - paddle_height // 2, paddle_width, paddle_height)
    opponent_paddle = pygame.Rect(WIDTH - 130, HEIGHT // 2 - paddle_height // 2, paddle_width, paddle_height)

# Reset ball and paddles when ever needed
def reset_ball_and_paddles():
    global ball, ball_dx, ball_dy, ball_speed
    ball_speed *= 1.1
    ball = pygame.Rect(WIDTH // 2 - ball_size // 2, HEIGHT // 2 - ball_size // 2, ball_size, ball_size)
    ball_dx, ball_dy = ball_speed, ball_speed
    reset_paddles()

# Ball movement
def move_ball():
    global ball_dx, ball_dy, player_score, opponent_score
    ball.x += ball_dx
    ball.y += ball_dy

    if ball.left <= 0:
        ball_dx = ball_speed
        opponent_score += 1
        reset_ball_and_paddles()
    elif ball.right >= WIDTH:
        ball_dx = -ball_speed
        player_score += 1
        reset_ball_and_paddles()
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

# Game loop
while player_score < winning_score and opponent_score < winning_score:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == STAMINA_RECHARGE_EVENT and stamina_blocks < MAX_STAMINA_BLOCKS and not boost_active:
            stamina_blocks += 1
        elif event.type == STAMINA_CONSUME_EVENT and boost_active:
            stamina_blocks = max(0, stamina_blocks - 1)

    move_paddles()
    move_ball()
    draw_objects()
    update_stamina()
    draw_stamina()

    pygame.display.flip()
screen.fill((0, 0, 0))  # Clear the screen before displaying the message
message = "You win!" if player_score > opponent_score else "You lose!"
message_text = font.render(message, True, WHITE)
screen.blit(message_text, (WIDTH // 2 - message_text.get_width() // 2, HEIGHT // 2 - message_text.get_height() // 2))
pygame.display.flip()

# Adds a delay before quitting the game
pygame.time.delay(3000)
pygame.quit()
sys.exit()

