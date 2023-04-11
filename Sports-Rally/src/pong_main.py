"""
A simple pvp Pong game implementation using Pygame.
"""

import sys
import pygame

pygame.init()

WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

FPS = 60
clock = pygame.time.Clock()

# Paddle and ball configurations
paddle_width, paddle_height = 20, 100
player_speed_normal = 5
player_speed_boosted = 8
opponent_speed_normal = 5
opponent_speed_boosted = 8
player_paddle = pygame.Rect(
    100, HEIGHT // 2 - paddle_height // 2, paddle_width, paddle_height)
opponent_paddle = pygame.Rect(
    WIDTH - 130, HEIGHT // 2 - paddle_height // 2, paddle_width, paddle_height)

ball_size = 20
ball_speed = 4
ball = pygame.Rect(WIDTH // 2 - ball_size // 2, HEIGHT //
                   2 - ball_size // 2, ball_size, ball_size)
ball_dx, ball_dy = ball_speed, ball_speed

# Score settings
player_score = 0
opponent_score = 0
winning_score = 10
font = pygame.font.Font(None, 36)

# Game loop
def game_loop():
    global player_score, opponent_score

    while player_score < winning_score and opponent_score < winning_score:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        move_paddles()
        move_ball()
        draw_objects()

        pygame.display.flip()

    show_winner()

# Moving paddles
def move_paddles():
    keys = pygame.key.get_pressed()

    if keys[pygame.K_w] and player_paddle.top > 0:
        player_paddle.y -= player_speed_normal
    if keys[pygame.K_s] and player_paddle.bottom < HEIGHT:
        player_paddle.y += player_speed_normal

    if keys[pygame.K_UP] and opponent_paddle.top > 0:
        opponent_paddle.y -= opponent_speed_normal
    if keys[pygame.K_DOWN] and opponent_paddle.bottom < HEIGHT:
        opponent_paddle.y += opponent_speed_normal

# Moving the ball
def move_ball():
    global ball_dx, ball_dy, player_score, opponent_score
    ball.x += ball_dx
    ball.y += ball_dy

    if ball.left <= 0:
        ball_dx = ball_speed
        opponent_score += 1
    elif ball.right >= WIDTH:
        ball_dx = -ball_speed
        player_score += 1
    elif ball.colliderect(player_paddle) and ball_dx < 0:
        ball_dx = ball_speed
    elif ball.colliderect(opponent_paddle) and ball_dx > 0:
        ball_dx = -ball_speed
    if ball.top <= 0 or ball.bottom >= HEIGHT:
        ball_dy *= -1

def draw_objects():
    """
    Draw game objects including paddles, ball, and score.
    """
    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, WHITE, player_paddle)
    pygame.draw.rect(screen, WHITE, opponent_paddle)
    pygame.draw.ellipse(screen, WHITE, ball)
    pygame.draw.aaline(screen, WHITE, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT))

    score_text = font.render(f"{player_score} - {opponent_score}", True, WHITE)
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 10))

def show_winner():
    """
    Show the winner message after the game ends.
    """
    screen.fill((0, 0, 0))  # Clear the screen before displaying the message
    message = "Player 1 wins!" if player_score > opponent_score else "Player 2 wins!"
    message_text = font.render(message, True, WHITE)
    screen.blit(message_text, (WIDTH // 2 - message_text.get_width() //
                2, HEIGHT // 2 - message_text.get_height() // 2))
    pygame.display.flip()

    # Adds a delay before quitting the game
    pygame.time.delay(3000)
    pygame.quit()
    sys.exit()

def main():
    """
    Main function to encapsulate the game loop.
    """
    game_loop()

if __name__ == "__main__":
    main()

