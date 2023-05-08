import pygame
import sys
import subprocess

# Button class
class Button:
    def __init__(self, x, y, width, height, text, font_size, text_color, button_color, action=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font_size = font_size
        self.text_color = text_color
        self.button_color = button_color
        self.action = action

    def draw(self, screen):
        pygame.draw.rect(screen, self.button_color, self.rect)
        draw_text_with_shadow(screen, self.text, self.font_size, self.rect.centerx, self.rect.centery, self.text_color)

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            return True
        return False

# Menu class
class Menu:
    def __init__(self, screen, background_image_path=None):
        self.screen = screen
        if background_image_path:
            self.background_image = pygame.image.load(background_image_path)
        else:
            self.background_image = None
        self.buttons = []

    def add_button(self, button):
        self.buttons.append(button)

    def draw(self):
        if self.background_image:
            self.screen.blit(self.background_image, (0, 0))
        for button in self.buttons:
            button.draw(self.screen)

    def handle_events(self, event):
        for button in self.buttons:
            if button.is_clicked(event):
                if button.action:
                    button.action()
                return True
        return False

# Text and shadow drawing function
def draw_text_with_shadow(screen, text, size, x, y, color, shadow_color=(100, 100, 100), offset=(2, 2)):
    font = pygame.font.Font(pygame.font.get_default_font(), size)
    text_surface = font.render(text, True, color)
    shadow_surface = font.render(text, True, shadow_color)
    text_rect = text_surface.get_rect()
    shadow_rect = shadow_surface.get_rect()
    text_rect.center = (x, y)
    shadow_rect.center = (x + offset[0], y + offset[1])
    screen.blit(shadow_surface, shadow_rect)
    screen.blit(text_surface, text_rect)

# Button action functions
def open_pong_practice():
    subprocess.Popen(['python', 'src/pong/pong_practice.py'])
    print("Starting practice mode...")

def open_pong_pvp():
    subprocess.Popen(['python', 'src/pong/pong_pvp.py'])
    print("Starting PvP mode...")

def exit_game():
    pygame.quit()
    sys.exit()

# Main function


