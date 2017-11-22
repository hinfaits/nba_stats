from sqlalchemy import create_engine
from datetime import datetime
import json
import functools

def date_to_dict(dt):
    return dict(
        year=dt.year,
        month=dt.month,
        day=dt.day)

def get_db():
    config = get_config()
    # return create_engine('sqlite:////tmp/nba.sqlite')
    return create_engine("mysql+mysqlconnector://{}:{}@{}/{}".format(
        config["sql_username"],
        config["sql_password"],
        config["sql_host"],
        config["sql_database"]))

@functools.lru_cache(maxsize=1024)
def get_config(pathname=None):
    default_paths = ["../config.json", "./config.json"]
    paths = [pathname] if pathname else default_paths
    for path in paths:
        try:
            with open(path) as file_input:
                config = json.load(file_input)
        except FileNotFoundError:
            continue
        else:
            return config
    raise IOError("Config file not found.")
