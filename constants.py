from datetime import date, time, datetime, timedelta

"""The day before the regular season opener"""
DATE_SEASON_START = date(2017, 10, 16)

"""Last possible date of a 17-18 season game"""
DATE_SEASON_END = date(2018, 4, 11)

"""Last possible date of a 17-18 post season game"""
# DATE_SEASON_END = date(2018, 6, 17)

"""Maps common game intervals to parameters for the official NBA API"""
PERIOD = {
    "GAME": {
        "start_period": 1,
        "end_period": 10,
        "start_range": 0,
        "end_range": 28800,
        "range_type": 0
    },
    "Q1": {
        "start_period":  1,
        "end_period":  10,
        "start_range":  0,
        "end_range":  7200,
        "range_type":  2
    },
    "Q2": {
        "start_period": 1,
        "end_period": 10,
        "start_range": 7200,
        "end_range": 14400,
        "range_type": 2
    },
    "Q3": {
        "start_period":  1,
        "end_period":  10,
        "start_range":  14400,
        "end_range":  21600,
        "range_type":  2
    },
    "Q4": {
        "start_period": 1,
        "end_period": 10,
        "start_range": 21600,
        "end_range": 28800,
        "range_type": 2
    },
    "H1": {
        "start_period": 1,
        "end_period": 10,
        "start_range": 0,
        "end_range": 14400,
        "range_type": 2
    },
    "H2": {
        "start_period": 1,
        "end_period": 10,
        "start_range": 14400,
        "end_range": 28800,
        "range_type": 2
    },
    "OT1": {
        "start_period": 1,
        "end_period": 10,
        "start_range": 28800,
        "end_range": 31800,
        "range_type": 2
    },
    "OT2": {
        "start_period": 1,
        "end_period": 10,
        "start_range": 28800 + 3000,
        "end_range": 31800 + 3000,
        "range_type": 2
    },
    "OT3": {
        "start_period": 1,
        "end_period": 10,
        "start_range": 14400 + 2 * 3000,
        "end_range": 28800 + 2 * 3000,
        "range_type": 2
    },
    "OT4": {
        "start_period": 1,
        "end_period": 10,
        "start_range": 14400 + 3 * 3000,
        "end_range": 28800 + 3 * 3000,
        "range_type": 2
    },
    "OT5": {
        "start_period": 1,
        "end_period": 10,
        "start_range": 14400 + 4 * 3000,
        "end_range": 28800 + 4 * 3000,
        "range_type": 2
    },
    "OT6": {
        "start_period": 1,
        "end_period": 10,
        "start_range": 14400 + 5 * 3000,
        "end_range": 28800 + 5 * 3000,
        "range_type": 2
    },
    "OT7": {
        "start_period": 1,
        "end_period": 10,
        "start_range": 14400 + 6 * 3000,
        "end_range": 28800 + 6 * 3000,
        "range_type": 2
    },
    "OT8": {
        "start_period": 1,
        "end_period": 10,
        "start_range": 14400 + 7 * 3000,
        "end_range": 28800 + 7 * 3000,
        "range_type": 2
    },
    "OT9": {
        "start_period": 1,
        "end_period": 10,
        "start_range": 14400 + 8 * 3000,
        "end_range": 28800 + 8 * 3000,
        "range_type": 2
    },
    "OT10": {
        "start_period": 1,
        "end_period": 10,
        "start_range": 14400 + 9 * 3000,
        "end_range": 28800 + 9 * 3000,
        "range_type": 2
    }
}
