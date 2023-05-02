import pygame
import sys
import random
import math
import pong_

class Paddle:
    """class for paddle control"""
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)

    def move(self, speed, direction, screen_height):
        """function for paddle movement"""
        if direction == "up" and self.rect.top > 0:
            self.rect.y -= speed
        elif direction == "down" and self.rect.bottom < screen_height:
            self.rect.y += speed

    def draw(self, screen, color):
        """function for drawing the paddles"""
        pygame.draw.rect(screen, color, self.rect)

class Ball:
    """class for ball related parameters"""
    def __init__(self, x, y, size, speed):
        self.rect = pygame.Rect(x, y, size, size)
        self.dx = speed
        self.dy = speed

    def move(self, screen_width, screen_height):
        """function for ball movement"""
        self.rect.x += self.dx
        self.rect.y += self.dy

        if self.rect.left <= 0 or self.rect.right >= screen_width:
            self.dx *= -1
        if self.rect.top <= 0 or self.rect.bottom >= screen_height:
            self.dy *= -1

    def draw(self, screen, color):
        """function for drawing the ball"""
        pygame.draw.ellipse(screen, color, self.rect)

class StaminaSystem:
    """class for the stamina system"""
    def __init__(self, max_blocks):
        self.blocks = 0
        self.max_blocks = max_blocks

    def update_stamina(self, boost_active):
        """updating stamina blocks"""
        if not boost_active and self.blocks < self.max_blocks:
            self.blocks += 1

    def consume_stamina(self):
        """stamina consumption"""
        if self.blocks > 0:
            self.blocks -= 1

    def draw_stamina(self, screen, x, color, HEIGHT):
        """stamina stack visualization"""
        block_width, block_height = 20, 10
        block_gap = 2

        for i in range(self.blocks):
            block_y = HEIGHT - (i + 1) * (block_height + block_gap)
            pygame.draw.rect(screen, color, (x, block_y, block_width, block_height))

class Score:
    """class for score"""
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.value = 0
        self.font = pygame.font.Font(None, 72)

    def draw(self, screen, color):
        """function for drawing score"""
        score_text = self.font.render(f"{self.value}", True, color)
        screen.blit(score_text, (self.x - score_text.get_width() // 2, self.y))

class ExitButton:
    """class for an exit button"""
    def __init__(self, x, y):
        self.width, self.height = 40, 40
        self.rect = pygame.Rect(x, y, self.width, self.height)

    def collidepoint(self, pos):
        """function for the collision of mouse and the button"""
        return self.rect.collidepoint(pos)

    def draw(self, screen, color):
        """function for drawing the button"""
        pygame.draw.rect(screen, color, self.rect, 3)
        pygame.draw.line(screen, color, (self.rect.left + 10, self.rect.top + 10),
                         (self.rect.right - 10, self.rect.bottom - 10), 3)
        pygame.draw.line(screen, color, (self.rect.left + 10, self.rect.bottom - 10),
                         (self.rect.right - 10, self.rect.top + 10), 3)


class SoundEffect:
    def __init__(self, file_name):
        """Initialize the SoundEffect class with the given sound file."""
        self.sound = pygame.mixer.Sound(file_name)

    def play(self):
        """Play the sound effect."""
        self.sound.play()