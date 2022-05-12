import unittest

from game_of_life.game_of_life import Game


class TestStringMethod(unittest.TestCase):

    def test_001_run_application(self):
        """
            Run application
        """

        Game(debug=True)


if __name__ == '__main__':
    unittest.main()