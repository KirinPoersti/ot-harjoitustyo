import unittest
from unittest.mock import Mock, patch
import pygame
from ..classes.menu_class import (
    SoundManager,
    Button,
    create_text_surface,
    create_shadow_surface,
    start_game,
)


class TestSoundManager(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.sound_manager = None

    def setUp(self):
        self.sound_manager = SoundManager()

    def test_play_paddle_sound(self):
        result = self.sound_manager.play_paddle_sound()
        self.assertEqual(result, "Sound played")

    def test_play_wall_sound(self):
        result = self.sound_manager.play_wall_sound()
        self.assertEqual(result, "Sound played")

    def test_play_pong_score_sound(self):
        result = self.sound_manager.play_pong_score_sound()
        self.assertEqual(result, "Sound played")

    def test_play_boosted_sound(self):
        result = self.sound_manager.play_boosted_sound()
        self.assertEqual(result, "Sound played")

    def test_play_button_sound(self):
        result = self.sound_manager.play_button_sound()
        self.assertEqual(result, "Sound played")

    def test_play_jump_sound(self):
        result = self.sound_manager.play_jump_sound()
        self.assertEqual(result, "Sound played")

    def test_play_longjump_score_sound(self):
        result = self.sound_manager.play_longjump_score_sound()
        self.assertEqual(result, "Sound played")

    def test_play_pong_bgm_sound(self):
        result = self.sound_manager.play_pong_bgm_sound()
        self.assertEqual(result, "Bgm played")

    def test_play_longjump_bgm_sound(self):
        result = self.sound_manager.play_longjump_bgm_sound()
        self.assertEqual(result, "Bgm played")

    def test_play_menu_bgm_sound(self):
        result = self.sound_manager.play_menu_bgm_sound()
        self.assertEqual(result, "Bgm played")


class TestFunctions(unittest.TestCase):
    @patch("pygame.font.Font")
    def test_create_text_surface(self, mock_font):
        mock_font.return_value.render.return_value = "rendered_text"
        result = create_text_surface("Hello", 32, (255, 255, 255))
        self.assertEqual(result, "rendered_text")

    @patch("pygame.font.Font")
    def test_create_shadow_surface(self, mock_font):
        mock_font.return_value.render.return_value = "shadow_surface"
        result = create_shadow_surface("Hello", 32, (0, 0, 0))
        self.assertEqual(result, "shadow_surface")

    @patch("pygame.display.set_mode")
    def draw_text_with_shadow(
        self, screen, text, size, object_x, object_y, color, shadow_color, offset=(2, 2)
    ):
        font = pygame.font.Font(pygame.font.get_default_font(), size)
        text_surface = font.render(text, True, color)
        shadow_surface = font.render(text, True, shadow_color)

        text_rect = text_surface.get_rect()
        text_rect.center = (object_x, object_y)

        shadow_rect = text_rect.copy()
        shadow_rect.x += offset[0]
        shadow_rect.y += offset[1]

        screen.blit(shadow_surface, shadow_rect)
        screen.blit(text_surface, text_rect)

    @patch("os.system")
    @patch("pygame.mixer.music")
    def test_start_game(self, mock_music, mock_os):
        start_game(["python", "pong.py"])
        mock_os.assert_called_once_with("python pong.py")
        mock_music.stop.assert_called_once()
        mock_music.play.assert_called_once_with(-1)


class TestButton(unittest.TestCase):
    def setUp(self):
        self.sound_manager = Mock()
        self.button = Button(0, 0, 200, 100, self.sound_manager)

    def test_collidepoint(self):
        self.assertTrue(self.button.collidepoint((50, 50)))
        self.assertFalse(self.button.collidepoint((250, 250)))

    @patch("pygame.draw.rect")
    def test_draw(self, mock_draw_rect):
        mock_screen = Mock()
        self.button = Button(0, 0, 200, 100, self.sound_manager)
        self.button.draw(mock_screen, "Hello", 32, (255, 255, 255), (0, 0, 0))
        mock_draw_rect.assert_called_once()

    @patch("pygame.draw.rect")
    @patch("pygame.draw.line")
    def test_draw_exit_button(self, mock_draw_line, mock_draw_rect):
        mock_screen = Mock()
        exit_button = self.button.draw_exit_button(mock_screen)
        self.assertIsInstance(exit_button, pygame.Rect)
        self.assertEqual(mock_draw_rect.call_count, 1)
        self.assertEqual(mock_draw_line.call_count, 2)

    def test_clicked(self):
        mock_command = Mock()
        self.button.clicked(True, mock_command)
        self.sound_manager.play_button_sound.assert_called_once()
        mock_command.assert_called_once()


if __name__ == "__main__":
    unittest.main()
