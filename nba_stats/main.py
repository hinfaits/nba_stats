import logging

from datetime import date
from datetime import timedelta

import boto3
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy import inspect

import nba
import utils
from helpers import get_periods
from dump import S3Dumper
from constants import DATE_SEASON_START, DATE_SEASON_END, PERIOD
from config import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY

# For debugging
from pprint import pprint
import traceback
import sys
import pdb

DEBUG = True

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def config_logging():
    log_format = "[%(asctime)s] %(name)s %(levelname)s: %(message)s"
    logging.basicConfig(level=logging.INFO,
                        format=log_format)

def games_to_scrape(conn):
    """Find games we need to get boxscores for"""
    headers = pd.read_sql_table("game_headers", conn)
    boxscores = pd.read_sql_table("bst_team_game", conn)

    # I don't know what `WH_STATUS` exactly is, but check it anyway
    played_games = headers[
        (headers["GAME_STATUS_TEXT"] == "Final") & (headers["WH_STATUS"] == 1)]
    played_games = played_games[['GAME_ID']].squeeze().tolist()
    saved_games = boxscores[['GAME_ID']].squeeze().tolist()
    return sorted(set(played_games) - set(saved_games))

def delete_from_tables(game_id, conn):
    """Delete all traces of a game_id from the database"""
    inspector = inspect(conn)
    for table_name in inspector.get_table_names():
        data_frame = pd.read_sql_table(table_name, conn)
        data_frame = data_frame[data_frame.GAME_ID != game_id]
        data_frame.to_sql(table_name, conn, index=False, if_exists="replace")

def full_update(conn):
    """Make our database upto date"""
    start_date = DATE_SEASON_START
    end_date = DATE_SEASON_END
    # end_date = date.today() - timedelta(days=2)

    schedule_results = nba.get_games(start_date, end_date)
    schedule_results.write_to_db(conn, if_exists="replace")

    new_games = games_to_scrape(conn)
    for game_id in new_games:
        logger.info("Fetching boxscores for game %s", game_id)
        boxscore_results = nba.get_all_boxscores(game_id,
                                             get_periods(game_id, conn))
        boxscore_results.write_to_db(conn, if_exists="append")

def main():
    config_logging()

    engine = utils.get_db()
    conn = engine.connect()
    full_update(conn)

    s3 = boto3.client('s3',
                      aws_access_key_id=AWS_ACCESS_KEY_ID,
                      aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
    S3Dumper.dump(conn, s3)

if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        if DEBUG:
            type, value, tb = sys.exc_info()
            traceback.print_exc()
            pdb.post_mortem(tb)
        else:
            raise exc
