import sys
import csv
import pygame
from ..classes.menu_class import SoundManager


pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GROUND_Y = SCREEN_HEIGHT - 10
PLAYER_START_POS = 100
FONT_COLOR = (255, 255, 255)
BACKGROUND_COLOR = (0, 0, 0)
GROUND_COLOR = (200, 200, 200)
PLAYER_COLOR = (255, 255, 255)
POLE_COLOR = (255, 100, 100)
FPS = 60
REGION_WIDTH = 135

LEADERBOARD_FILE = "src/resources/leaderboard.csv"

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Long Jump")
clock = pygame.time.Clock()

sound_manager = SoundManager()


def draw_text(text, size, object_x, object_y, color):
    font = pygame.font.Font(pygame.font.get_default_font(), size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (object_x, object_y)
    screen.blit(text_surface, text_rect)


def draw_region_lines():
    region_line_x_values = [125, 260, 395, 530, 665]
    region_line_meters = [1, 2.5, 5, 7.5, 10]
    for i, x in enumerate(region_line_x_values):
        meters = region_line_meters[i]
        draw_text(f"{meters}m", 20, x, GROUND_Y - 30, FONT_COLOR)
        pygame.draw.line(
            screen, GROUND_COLOR, (x, GROUND_Y - 20), (x, GROUND_Y + 20), 2
        )


def get_player_name():
    input_text = ""
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                elif event.key == pygame.K_RETURN:
                    return input_text
                else:
                    input_text += event.unicode
        screen.fill(BACKGROUND_COLOR)
        draw_text(
            "Enter your name:",
            32,
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2 - 48,
            FONT_COLOR,
        )
        draw_text(
            input_text,
            32,
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2,
            FONT_COLOR,
        )
        pygame.display.flip()
        clock.tick(FPS)


def calculate_landing_point(score):
    if score <= 1:
        landing_point = (score - 0) / (1 - 0)
    elif score <= 2.5:
        landing_point = 125 + 135 * (score - 1) / (2.5 - 1)
    elif score <= 5:
        landing_point = 260 + 135 * (score - 2.5) / (5 - 2.5)
    elif score <= 7.5:
        landing_point = 395 + 135 * (score - 5) / (7.5 - 5)
    else:
        landing_point = 530 + 135 * (score - 7.5) / (10 - 7.5)
    return landing_point


def save_score(name, score):
    with open(LEADERBOARD_FILE, "a", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([name, score])


def display_leaderboard():
    scores = load_scores(LEADERBOARD_FILE)
    scores.sort(key=lambda x: x[1], reverse=True)

    screen.fill((0, 0, 0))

    font = pygame.font.Font(None, 36)
    text_color = (255, 255, 255)

    for i, (player_name, score) in enumerate(scores):
        text = font.render(f"{i + 1}. {player_name}: {score}", True, text_color)
        screen.blit(text, (50, 50 + i * 40))

    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    done = True

        pygame.display.flip()


def load_scores(file_path):
    scores = []
    with open(file_path, "r", encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            scores.append((row[0], float(row[1])))
    scores.sort(key=lambda x: x[1], reverse=True)
    return scores


def quadratic_bezier(t_0, p_0, p_1, p_2):
    return (1 - t_0) ** 2 * p_0 + 2 * (1 - t_0) * t_0 * p_1 + t_0**2 * p_2


def player_jump(player_rect, landing_point):
    jump_speed = 200 / FPS
    jump_height = 50

    while player_rect.y > GROUND_Y - 50 - jump_height:
        player_rect.y -= jump_speed
        screen.fill(BACKGROUND_COLOR)
        pygame.draw.line(
            screen, GROUND_COLOR, (0, GROUND_Y), (SCREEN_WIDTH, GROUND_Y), 5
        )
        draw_region_lines()
        pygame.draw.rect(screen, PLAYER_COLOR, player_rect)
        pygame.display.flip()
        clock.tick(FPS)

    while player_rect.x < landing_point:
        player_rect.x += jump_speed
        if player_rect.y < GROUND_Y - 50:
            player_rect.y += jump_speed
        screen.fill(BACKGROUND_COLOR)
        pygame.draw.line(
            screen, GROUND_COLOR, (0, GROUND_Y), (SCREEN_WIDTH, GROUND_Y), 5
        )
        draw_region_lines()
        pygame.draw.rect(screen, PLAYER_COLOR, player_rect)
        pygame.display.flip()
        clock.tick(FPS)


def game_loop():
    sound_manager.play_longjump_bgm_sound()
    player_rect = pygame.Rect(PLAYER_START_POS, GROUND_Y - 50, 25, 50)
    pole_rect = pygame.Rect(SCREEN_WIDTH, GROUND_Y - 150, 10, 150)
    pole_speed = 200 / FPS

    left_pressed = False
    right_pressed = False
    sets = 0
    speed_built = 0

    countdown_timer = pygame.time.get_ticks()
    speed_timer = 0
    fail_timer = 0

    game_state = "countdown"

    attempts = 3

    attempt_scores = []

    while True:
        screen.fill(BACKGROUND_COLOR)

        pygame.draw.line(
            screen, GROUND_COLOR, (0, GROUND_Y), (SCREEN_WIDTH, GROUND_Y), 5
        )

        pygame.draw.rect(screen, PLAYER_COLOR, player_rect)
        pygame.draw.rect(screen, POLE_COLOR, pole_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if game_state == "speed_building":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        left_pressed = True
                    if event.key == pygame.K_RIGHT:
                        right_pressed = True
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        left_pressed = False
                    if event.key == pygame.K_RIGHT:
                        right_pressed = False

            if game_state == "jump":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        game_state = "settlement"

        if game_state == "countdown":
            remaining_time = 3 - (pygame.time.get_ticks() - countdown_timer) // 1000
            if remaining_time >= 1:
                draw_text(
                    str(remaining_time),
                    48,
                    SCREEN_WIDTH // 2,
                    SCREEN_HEIGHT // 2,
                    FONT_COLOR,
                )
            else:
                game_state = "speed_building"
                speed_timer = pygame.time.get_ticks()
                countdown_timer += 3000

        elif game_state == "speed_building":
            draw_text(
                "Press <- and ->", 32, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, FONT_COLOR
            )
            elapsed_time = (pygame.time.get_ticks() - speed_timer) // 1000
            if elapsed_time < 5:
                if left_pressed and right_pressed:
                    sets += 1
                    speed_built += 1
                    left_pressed = False
                    right_pressed = False

                pole_rect.x -= pole_speed
                if pole_rect.colliderect(player_rect):
                    game_state = "jump"
                elif pole_rect.x + pole_rect.width < player_rect.x:
                    game_state = "failed"

        elif game_state == "jump":
            draw_text("Jump!", 48, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, FONT_COLOR)

        elif game_state == "settlement":
            draw_region_lines()
            if sets <= 5:
                score = 1
            elif sets <= 15:
                score = 1 + (sets - 5) * (1.5 / 10)
            elif sets <= 25:
                score = 2.5 + (sets - 15) * (2.5 / 10)
            elif sets <= 35:
                score = 5 + (sets - 25) * (2.5 / 10)
            elif sets <= 45:
                score = 7.5 + (sets - 35) * (2.5 / 10)
            else:
                score = 10
            sound_manager.play_jump_sound()

            landing_point = calculate_landing_point(score)
            player_jump(player_rect, landing_point)

            attempt_scores.append(score)
            attempts -= 1

            if attempts == 0:
                game_state = "end_game"
            else:
                game_state = "countdown"
                countdown_timer = pygame.time.get_ticks()
                pole_rect.x = SCREEN_WIDTH
                sets = 0
                speed_built = 0

                player_rect.x = PLAYER_START_POS
                player_rect.y = GROUND_Y - 50

            draw_region_lines()
            draw_text(
                f"Score: {score:.2f}m",
                32,
                SCREEN_WIDTH // 2,
                SCREEN_HEIGHT // 2,
                FONT_COLOR,
            )

            pygame.display.flip()
            pygame.time.delay(2000)
            sound_manager.play_longjump_score_sound()

        elif game_state == "failed":
            if fail_timer == 0:
                fail_timer = pygame.time.get_ticks()

            if (pygame.time.get_ticks() - fail_timer) // 1000 < 2:
                draw_text("Failed attempt", 32, SCREEN_WIDTH // 2, 10, FONT_COLOR)
            else:
                game_state = "countdown"
                countdown_timer = pygame.time.get_ticks()
                pole_rect.x = SCREEN_WIDTH
                fail_timer = 0

        elif game_state == "end_game":
            best_score = max(attempt_scores)
            draw_text(
                "Attempts finished",
                32,
                SCREEN_WIDTH // 2,
                SCREEN_HEIGHT // 2 - 32,
                FONT_COLOR,
            )
            for idx, score in enumerate(attempt_scores):
                draw_text(
                    f"Attempt {idx + 1}: {score:.2f}m",
                    24,
                    SCREEN_WIDTH - 150,
                    50 + idx * 24,
                    FONT_COLOR,
                )

            pygame.display.flip()
            pygame.time.delay(5000)

            # Get player's name and save their best score
            player_name = get_player_name()
            save_score(player_name, best_score)

            # Load leaderboard and display it
            leaderboard = load_scores()
            leaderboard.sort(key=lambda x: -float(x[1]))
            for idx, (name, score) in enumerate(leaderboard):
                draw_text(
                    f"{idx+1}. {name}: {score}m",
                    24,
                    50,
                    50 + idx * 24,
                    FONT_COLOR,
                )

            pygame.display.flip()
            pygame.time.delay(10000)
            break

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    game_loop()