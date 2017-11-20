from sqlalchemy import create_engine

from config import SQL_USERNAME, SQL_PASSWORD, SQL_HOST, SQL_DATABASE

def date_to_dict(dt):
    return dict(
        year=dt.year,
        month=dt.month,
        day=dt.day)

def get_db():
    # return create_engine('sqlite:////tmp/nba.sqlite')
    return create_engine("mysql+mysqlconnector://{}:{}@{}/{}".format(
        SQL_USERNAME,
        SQL_PASSWORD,
        SQL_HOST,
        SQL_DATABASE))
