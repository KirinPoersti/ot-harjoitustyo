import pygame
import sys
import random
import math

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Create screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

# Initialize clock
FPS = 60
clock = pygame.time.Clock()

# Paddle
paddle_width, paddle_height = 20, 100
paddle_speed = 5
player_paddle = pygame.Rect(100, HEIGHT // 2 - paddle_height // 2, paddle_width, paddle_height)

# Ball
ball_size = 20
ball_speed = 4.5
ball = pygame.Rect(WIDTH // 2 - ball_size // 2, HEIGHT // 2 - ball_size // 2, ball_size, ball_size)
ball_dx, ball_dy = random.choice([-1, 1]) * ball_speed, random.choice([-1, 1]) * ball_speed

# Shooter block
shooter_block = pygame.Rect(WIDTH - 130, HEIGHT // 2 - paddle_height // 2, paddle_width, paddle_height)

# Score
player_score = 0
font = pygame.font.Font(None, 72)

# Exit button
button_width, button_height = 40, 40
exit_button = pygame.Rect(WIDTH - button_width - 10, 10, button_width, button_height)

# Reset ball
def reset_ball():
    global ball, ball_dx, ball_dy
    ball.center = shooter_block.center  
    angle = random.uniform(math.radians(315), math.radians(405))
    ball_dx, ball_dy = -ball_speed * math.cos(angle), ball_speed * math.sin(angle)

# Move player paddle
def move_paddle():
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and player_paddle.top > 0:
        player_paddle.y -= paddle_speed
    if keys[pygame.K_s] and player_paddle.bottom < HEIGHT:
        player_paddle.y += paddle_speed

# Move ball
def move_ball():
    global ball_dx, ball_dy, player_score
    ball.x += ball_dx
    ball.y += ball_dy

    if ball.right >= WIDTH or ball.left <= 0:
        reset_ball()
    elif ball.colliderect(player_paddle) and ball_dx < 0:
        ball_dx = abs(ball_dx)
        player_score += 1
        reset_ball()
    if ball.top <= 0 or ball.bottom >= HEIGHT:
        ball_dy *= -1

# Shooter block
shooter_block_size = 100
shooter_block = pygame.Rect(WIDTH - 130, HEIGHT // 2 - shooter_block_size // 2, shooter_block_size, shooter_block_size)

# Draw objects
def draw_objects():
    screen.fill(BLACK)
    pygame.draw.rect(screen, WHITE, player_paddle)
    pygame.draw.rect(screen, WHITE, shooter_block)
    pygame.draw.ellipse(screen, WHITE, ball)
    score_text = font.render(f"{player_score}", True, WHITE)
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 10))
    pygame.draw.aaline(screen, WHITE, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT)) 

# Exit button
    pygame.draw.rect(screen, BLACK, exit_button)
    pygame.draw.rect(screen, WHITE, exit_button, 3) 
    pygame.draw.line(screen, WHITE, (exit_button.left + 10, exit_button.top + 10), (exit_button.right - 10, exit_button.bottom - 10), 3)
    pygame.draw.line(screen, WHITE, (exit_button.left + 10, exit_button.bottom - 10), (exit_button.right - 10, exit_button.top + 10), 3)

# Main game loop
reset_ball() 
while True:
    clock.tick(FPS)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if exit_button.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

    # Move paddle and ball
    move_paddle()
    move_ball()
    # Draw objects
    draw_objects()
     
    pygame.display.flip()
