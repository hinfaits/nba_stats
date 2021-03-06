import unittest
import os

import pandas
from datetime import date

import nba

# These tests do calls to the nba_api and take upto 2 minutes to run due to rate limiting

@unittest.skipIf(os.environ.get("TRAVIS"), "Don't run this test on travis.")
class TestNbaGetGames(unittest.TestCase):

    def test_return_type(self):
        """
        Check calls to `get_games` returns a `ResultSet` object with the two
        expected dataframes
        """
        d = date(year=2017, month=11, day=2)

        results = nba.get_games(d, d)
        self.assertIsInstance(results, nba.ResultSet)

        results_dict = results.get_all()
        self.assertIsInstance(results_dict, dict)
        self.assertIsInstance(results_dict["game_headers"], pandas.DataFrame)
        self.assertIsInstance(results_dict["game_scores"], pandas.DataFrame)

    def test_games_fetched(self):
        """
        Check calls to `get_games` returns correct sized dataframe
        """
        start_date = date(year=2017, month=10, day=27)
        end_date = date(year=2017, month=10, day=30)

        results = nba.get_games(start_date, end_date)
        headers = results.get("game_headers")
        self.assertEqual(len(headers), 31)


@unittest.skipIf(os.environ.get("TRAVIS"), "Don't run this test on travis.")
class TestNbaGetBoxscores(unittest.TestCase):

    def test_it(self):
        """
        Check calls to `get_all_boxscores` returns correct amount of
        boxscores/dataframes
        """
        game_id = "0021700032"
        periods = ["game", "h1", "h2", "q1", "q2", "q3", "q4"]

        results = nba.get_all_boxscores(game_id, periods)

        self.assertIsInstance(results, nba.ResultSet)

        results_dict = results.get_all()
        self.assertEqual(len(results_dict), 94)

        for key, value in results_dict.items():
            self.assertIsInstance(key, str)
            self.assertIsInstance(value, pandas.DataFrame)


if __name__ == '__main__':
    unittest.main()
