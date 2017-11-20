import logging
from datetime import date
from datetime import timedelta
import pandas as pd

from helpers import get_periods
import utils
from constants import PERIOD
import nba.nba_api

logger = logging.getLogger(__name__)

class ResultSet(object):
    """Used for storing and returning dataframe(s) from nba-getter methods"""

    def __init__(self):
        self.result_dict = dict()

    def add(self, name, data_frame):
        self.result_dict[name] = data_frame

    def get(self, name):
        return self.result_dict[name]

    def get_all(self):
        return self.result_dict

    def write_to_db(self, conn, if_exists, index=False):
        for name, data_frame in self.result_dict.items():
            data_frame.to_sql(name, conn, index=index, if_exists=if_exists)


def get_games(start_date, end_date):
    """Get tables that represent the NBA schedule"""
    date_cursor = start_date
    logger.info("Getting scoreboards from %s to %s",
                start_date.strftime('%Y-%m-%d'),
                end_date.strftime('%Y-%m-%d'))
    while date_cursor <= end_date:
        scoreboard = nba_api.scoreboard(**utils.date_to_dict(date_cursor))
        logger.info("Fetched scoreboard for %s. Found %s games.",
                    date_cursor.strftime('%Y-%m-%d'),
                    len(scoreboard.game_header()))
        try:
            headers = pd.concat([headers, scoreboard.game_header()])
            scores = pd.concat([scores, scoreboard.line_score()])
        except NameError:
            logger.info("Initialized return arrays.")
            headers = scoreboard.game_header()
            scores = scoreboard.line_score()
        date_cursor = date_cursor + timedelta(days=1)

    result_set = ResultSet()
    result_set.add("game_headers", headers)
    result_set.add("game_scores", scores)
    return result_set

def get_all_boxscores(game_id, periods):
    """Get all boxscores for one game, and put them into the database

    """
    result_set = ResultSet()

    for period in periods:
        period_params = PERIOD[period.upper()]

        bst = nba_api.boxscore_traditional(game_id, **period_params)
        result_set.add("bst_team_" + period, bst.team_stats())
        result_set.add("bst_players_" + period, bst.player_stats())
        result_set.add("bst_team_bench_" + period, bst.team_starter_bench_stats())

        bss = nba_api.boxscore_scoring(game_id, **period_params)
        result_set.add("bss_team_" + period, bss.sql_team_scoring())
        result_set.add("bss_players_" + period, bss.sql_players_scoring())

        bsm = nba_api.boxscore_misc(game_id, **period_params)
        result_set.add("bsm_team_" + period, bsm.sql_team_misc())
        result_set.add("bsm_players_" + period, bsm.sql_players_misc())

        bsa = nba_api.boxscore_advanced(game_id, **period_params)
        result_set.add("bsa_team_" + period, bsa.sql_team_advanced())
        result_set.add("bsa_players_" + period, bsa.sql_players_advanced())

        bsf = nba_api.boxscore_four_factors(game_id, **period_params)
        result_set.add("bsf_team_" + period, bsf.sql_team_four_factors())
        result_set.add("bsf_players_" + period, bsf.sql_players_four_factors())

        bsu = nba_api.boxscore_usage(game_id, **period_params)
        result_set.add("bsu_team_" + period, bsu.sql_team_usage())
        result_set.add("bsu_players_" + period, bsu.sql_players_usage())

    # TODO: append "_game" to all of the following name strings
    bsh = nba_api.boxscore_hustle(game_id)
    result_set.add("bsh_team", bsh.hustle_stats_team_box_score())
    result_set.add("bsh_players", bsh.hustle_stats_player_box_score())

    pt = nba_api.boxscore_player_tracking(game_id)
    result_set.add("bs_player_tracking", pt.info())

    return result_set


def get_player_list():
    """Get all leauge players"""

def get_team_list():
    """Get all league teams"""


def get_all_player_stats(player_id):
    """Get all statlines for one player"""


def get_team_stats(team_id):
    """Get all statlines for one team"""
