import unittest
from unittest import mock

try:
    # For Py2, this version of StringIO is untested
    from StringIO import StringIO
except ImportError:
    # For Py3
    from io import StringIO

import pandas as pd

import helpers

headers_csv = """,GAME_DATE_EST,GAME_SEQUENCE,GAME_ID,TEAM_ID,TEAM_ABBREVIATION,TEAM_CITY_NAME,TEAM_WINS_LOSSES,PTS_QTR1,PTS_QTR2,PTS_QTR3,PTS_QTR4,PTS_OT1,PTS_OT2,PTS_OT3,PTS_OT4,PTS_OT5,PTS_OT6,PTS_OT7,PTS_OT8,PTS_OT9,PTS_OT10,PTS,FG_PCT,FT_PCT,FG3_PCT,AST,REB,TOV
    224,2017-11-01T00:00:00,9,0021700113,1610612750,MIN,Minnesota,5-3,31.0,34.0,18.0,21.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,104.0,0.494,0.667,0.273,20.0,47.0,21.0
    225,2017-11-01T00:00:00,9,0021700113,1610612740,NOP,New Orleans,3-5,28.0,26.0,23.0,21.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,98.0,0.429,0.857,0.258,27.0,38.0,19.0
    226,2017-11-01T00:00:00,10,0021700114,1610612761,TOR,Toronto,4-3,19.0,27.0,25.0,40.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,111.0,0.494,0.64,0.355,20.0,38.0,13.0
    227,2017-11-01T00:00:00,10,0021700114,1610612743,DEN,Denver,4-4,34.0,26.0,43.0,26.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,129.0,0.534,0.655,0.5,35.0,43.0,12.0
    228,2017-11-01T00:00:00,11,0021700115,1610612757,POR,Portland,4-4,20.0,19.0,30.0,25.0,9.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,103.0,0.398,0.741,0.265,17.0,53.0,17.0
    229,2017-11-01T00:00:00,11,0021700115,1610612762,UTA,Utah,5-3,22.0,17.0,25.0,30.0,18.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,112.0,0.378,0.861,0.448,16.0,55.0,14.0
    230,2017-11-01T00:00:00,12,0021700116,1610612742,DAL,Dallas,1-8,29.0,19.0,29.0,21.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,98.0,0.393,0.8,0.333,20.0,38.0,14.0
    231,2017-11-01T00:00:00,12,0021700116,1610612746,LAC,LA,5-2,32.0,34.0,29.0,24.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,119.0,0.526,0.828,0.464,27.0,49.0,16.0
    232,2017-11-02T00:00:00,1,0021700117,1610612744,GSW,Golden State,6-3,24.0,26.0,34.0,28.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,112.0,0.518,0.75,0.5,30.0,41.0,14.0
    233,2017-11-02T00:00:00,1,0021700117,1610612759,SAS,San Antonio,4-4,33.0,22.0,23.0,14.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,92.0,0.391,0.739,0.292,19.0,46.0,16.0
    234,2017-11-02T00:00:00,2,0021700118,1610612747,LAL,Los Angeles,3-5,25.0,37.0,23.0,25.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,110.0,0.544,0.741,0.222,16.0,32.0,11.0
    235,2017-11-02T00:00:00,2,0021700118,1610612757,POR,Portland,5-4,41.0,25.0,21.0,26.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,113.0,0.465,0.889,0.409,22.0,41.0,12.0
    2456,2018-04-11T00:00:00,11,0021701229,1610612757,POR,Portland,8-6,,,,,,,,,,,,,,,,,,,,,
    2457,2018-04-11T00:00:00,11,0021701229,1610612762,UTA,Utah,6-9,,,,,,,,,,,,,,,,,,,,,
    2458,2018-04-11T00:00:00,12,0021701230,1610612758,SAC,Sacramento,3-11,,,,,,,,,,,,,,,,,,,,,
    2459,2018-04-11T00:00:00,12,0021701230,1610612745,HOU,Houston,12-4,,,,,,,,,,,,,,,,,,,,,"""

@mock.patch("helpers.pd")
class TestGetOT(unittest.TestCase):
    csv_sio = StringIO(headers_csv)
    test_df = pd.read_csv(csv_sio, dtype={"GAME_ID": str})

    def test_no_ot(self, mock_pd):
        mock_pd.read_sql_table = mock.MagicMock(return_value=self.test_df)
        ret_value = helpers.get_ot("0021700116", None)
        self.assertEqual(ret_value[0], None)
        self.assertEqual(ret_value[1], 0)

    def test_is_ot(self, mock_pd):
        mock_pd.read_sql_table = mock.MagicMock(return_value=self.test_df)
        ret_value = helpers.get_ot("0021700115", None)
        self.assertEqual(ret_value[0], "OT1")
        self.assertEqual(ret_value[1], 1)

    def test_no_game_found(self, mock_pd):
        mock_pd.read_sql_table = mock.MagicMock(return_value=self.test_df)
        self.assertRaises(ValueError, helpers.get_ot, "0021601230", None)

@mock.patch("helpers.pd")
class TestGetPeriods(unittest.TestCase):
    csv_sio = StringIO(headers_csv)
    test_df = pd.read_csv(csv_sio, dtype={"GAME_ID": str})

    def test_no_ot(self, mock_pd):
        mock_pd.read_sql_table = mock.MagicMock(return_value=self.test_df)
        ret_value = helpers.get_periods("0021700116", None)
        self.assertEqual(ret_value,
                         ['game', 'h1', 'h2', 'q1', 'q2', 'q3', 'q4'])

    def test_is_ot(self, mock_pd):
        mock_pd.read_sql_table = mock.MagicMock(return_value=self.test_df)
        ret_value = helpers.get_periods("0021700115", None)
        self.assertEqual(ret_value,
                         ['game', 'h1', 'h2', 'q1', 'q2', 'q3', 'q4', 'ot1'])

    def test_no_game_found(self, mock_pd):
        mock_pd.read_sql_table = mock.MagicMock(return_value=self.test_df)
        self.assertRaises(ValueError, helpers.get_periods, "0021601230", None)
