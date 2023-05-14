import unittest
from unittest.mock import patch, mock_open
import pygame
from ..longjump.longjump import (
    LEADERBOARD_FILE,
    calculate_landing_point,
    save_score,
    load_scores,
)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FONT_COLOR = (255, 255, 255)
FPS = 60

GROUND_Y = SCREEN_HEIGHT - 10
PLAYER_START_POS = 100
BACKGROUND_COLOR = (0, 0, 0)
GROUND_COLOR = (200, 200, 200)
PLAYER_COLOR = (255, 255, 255)
POLE_COLOR = (255, 100, 100)
REGION_WIDTH = 135


class TestGameFunctions(unittest.TestCase):
    def setUp(self):
        self.screen = pygame.Surface((800, 600))

    def test_calculate_landing_point(self):
        self.assertEqual(calculate_landing_point(0.5), 0.5)
        self.assertEqual(calculate_landing_point(1.5), 170)
        self.assertEqual(calculate_landing_point(3.5), 314)
        self.assertEqual(calculate_landing_point(6), 449)
        self.assertEqual(calculate_landing_point(8.5), 584)

    @patch("csv.writer")
    @patch("builtins.open", new_callable=mock_open)
    def test_save_score(self, mock_file, mock_csv_writer):
        save_score("Test", 1.23)
        mock_file.assert_called_once_with(
            LEADERBOARD_FILE, "a", newline="", encoding="utf-8"
        )
        mock_csv_writer().writerow.assert_called_once_with(["Test", "1.23"])

    @patch("csv.reader")
    @patch("builtins.open", new_callable=mock_open)
    def test_load_scores(self, _, mock_csv_reader):
        mock_csv_reader.return_value = [["Test", "1.23"]]
        scores = load_scores(LEADERBOARD_FILE)
        self.assertEqual(scores, [("Test", 1.23)])


if __name__ == "__main__":
    unittest.main()
