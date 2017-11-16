from sqlalchemy import create_engine

def date_to_dict(dt):
    return dict(
        year=dt.year,
        month=dt.month,
        day=dt.day)

def get_db():
    sql_username = "np"
    sql_password = "eTeRmDoBZwOShWdJwaz1"
    sql_host = "np.iamaaronlol.com"
    sql_database = "test_db"
    # return create_engine('sqlite:////tmp/nba.sqlite')
    return create_engine("mysql+mysqlconnector://{}:{}@{}/{}".format(
        sql_username,
        sql_password,
        sql_host,
        sql_database))
