import pandas as pd

def is_ot(game_id, conn):
    """Returns the last OT period played in a game via the database

    Looks up `game_id` in the table `game_scores` and implicitly finds the last
    period of OT played by looking at the points scored.

    The most OT periods ever played has been 6. The NBA API supports upto 10 OT
    periods.

    Args:
        game_id (str): The game_id to look up in the database
        conn: SQLAlchemy Connection object

    Returns:
        (None, 0) [tuple] if no OT was played, or 

        A tuple with a string and integer pair containing the last OT period
        played up to OT10, the max returned by the NBA API. For example:

        ("OT1", 1) or ("OT2", 2) upto ("OT10", 10)

    Raises:
        ValueError: if no results found for input game_id in the database

    """
    game_scores = pd.read_sql_table("game_scores", conn)
    target = game_scores.loc[game_scores['GAME_ID'] == game_id]

    if target.empty:
        raise ValueError("game_id {} returned no results".format(game_id))

    for i in range(10, 0, -1):
        OT = "OT" + str(i)
        index = "PTS_" + OT
        if target[[index]].max()[0] > 0:
            return OT, i,

    return None, 0,


def get_periods(game_id, conn):
    """Get a list of the periods played in a given NBA game

    Args:
        game_id (str): The game_id to look up in the database
        conn: SQLAlchemy Connection object

    Returns:
        A list containing all periods played in a game. For example:
        ["game", "h1", "h2", "q1", "q2", "q3", "q4"]
        ["game", "h1", "h2", "q1", "q2", "q3", "q4", "ot1", "ot2"]

    Raises:
        ValueError: no results found for input game_id

    """
    periods = ["game", "h1", "h2", "q1", "q2", "q3", "q4"]
    ot_str, ot_int = is_ot(game_id, conn)
    for ot in range(1, 1 + ot_int):
        periods.append("ot" + str(ot))
    return periods
