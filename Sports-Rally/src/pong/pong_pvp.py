import pygame
import pygame.mixer
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

pygame.mixer.init()
pygame.mixer.music.load("src/resources/pong_bgm.mp3")
pygame.mixer.music.set_volume(0.25)
pygame.mixer.music.play(-1)  

class SoundManager:
    def __init__(self):
        pygame.mixer.init()
        self.paddle_sound = pygame.mixer.Sound("src/resources/pong_paddle.mp3")
        self.wall_sound = pygame.mixer.Sound("src/resources/pong_wall.mp3")
        self.score_sound = pygame.mixer.Sound("src/resources/pong_score.mp3")
        self.boosted_sound = pygame.mixer.Sound("src/resources/pong_boosted.mp3")
        self.button_sound = pygame.mixer.Sound("src/resources/button.mp3")

    def play_paddle_sound(self):
        self.paddle_sound.play()

    def play_wall_sound(self):
        self.wall_sound.play()

    def play_score_sound(self):
        self.score_sound.play()

    def play_boosted_sound(self):
        self.boosted_sound.play()

    def play_button_sound(self):
        self.button_sound.play()

sound_manager = SoundManager()

# Stamina handling
def handle_stamina(keys, stamina_blocks, stamina_recharge_timer, stamina_consume_timer, boost_key, prev_key_state):
    """
    Handles stamina consumption and recharge for a player based on their boost key state.
    
    Args:
        keys: List of key states from pygame.key.get_pressed().
        stamina_blocks: Number of stamina blocks available for the player.
        stamina_recharge_timer: Timer for stamina recharge.
        stamina_consume_timer: Timer for stamina consumption.
        boost_key: Key for boosting the player's speed (pygame.K_LSHIFT or pygame.K_RSHIFT).
        prev_key_state: Previous state of the boost key.
        
    Returns:
        Tuple with the following elements:
            boost_active: Bool indicating if boost is active.
            stamina_blocks: Updated number of stamina blocks.
            stamina_recharge_timer: Updated timer for stamina recharge.
            stamina_consume_timer: Updated timer for stamina consumption.
            prev_key_state: Updated previous state of the boost key.
    """
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
    """
    Draws the stamina blocks for both players on the game screen.
    """
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
    """
    Moves the paddles based on user input and handles speed boosting.
    """
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
    if boost_active:
        sound_manager.play_boosted_sound()


def calculate_opponent_target_y(ball_y, paddle_height, ball_height):
    """
    Calculates the target y-coordinate for the opponent paddle to follow the ball.
    
    Args:
        ball_y: The y-coordinate of the ball.
        paddle_height: The height of the paddle.
        ball_height: The height of the ball.
        
    Returns:
        The target y-coordinate for the opponent paddle.
    """
    return ball_y - (paddle_height - ball_height) // 2

def adjust_opponent_paddle_y(paddle_y, target_y, speed):
    """
    Adjusts the opponent paddle's y-coordinate to move towards the target y-coordinate.
    
    Args:
        paddle_y: The current y-coordinate of the opponent paddle.
        target_y: The target y-coordinate for the opponent paddle.
        speed: The speed at which the opponent paddle moves.
        
    Returns:
        The updated y-coordinate for the opponent paddle.
    """
    if paddle_y < target_y:
        return paddle_y + min(speed, target_y - paddle_y)
    elif paddle_y > target_y:
        return paddle_y - min(speed, paddle_y - target_y)
    return paddle_y

# Reseting ball after point is granted
def reset_ball(granter):
    """
    Resets the ball to its starting position and updates its direction.
    
    Args:
        granter: A string indicating which player scored the last point ("opponent" or "player").
    """
    global ball, ball_dx, ball_dy, ball_speed
    ball = pygame.Rect(WIDTH // 2 - ball_size // 2, HEIGHT //
                       2 - ball_size // 2, ball_size, ball_size)
    ball_dx, ball_dy = ball_speed, ball_speed

    if granter == "opponent":
        ball_dx = ball_speed 
    elif granter == "player":
        ball_dx = -ball_speed
    sound_manager.play_score_sound() 

# Ball movement
def move_ball():
    """
    Moves the ball based on its current speed and direction, and handles collisions with paddles and screen edges.
    Also updates player scores if the ball goes off the screen.
    """
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
        sound_manager.play_paddle_sound()
    elif ball.colliderect(opponent_paddle) and ball_dx > 0:
        ball_dx = -ball_speed
        sound_manager.play_paddle_sound()
    if ball.top <= 0 or ball.bottom >= HEIGHT:
        ball_dy *= -1
        sound_manager.play_wall_sound()


# Displaying game objects
def draw_objects():
    """
    Draws game objects including paddles, ball, and score on the screen.
    """
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