import unittest
from unittest.mock import patch, mock_open
from ..longjump.longjump import (
    LEADERBOARD_FILE,
    calculate_landing_point,
    save_score,
    load_scores,
    quadratic_bezier,
)


class TestGameFunctions(unittest.TestCase):
    def test_calculate_landing_point(self):
        self.assertEqual(calculate_landing_point(0.5), 0.5)
        self.assertEqual(calculate_landing_point(1.5), 170)
        self.assertEqual(calculate_landing_point(3.5), 314)
        self.assertEqual(calculate_landing_point(6), 449)
        self.assertEqual(calculate_landing_point(8.5), 584)

    def test_quadratic_bezier(self):
        self.assertEqual(quadratic_bezier(0.5, 0, 1, 2), 1)
        self.assertEqual(quadratic_bezier(0.75, 0, 1, 2), 1.5)

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
