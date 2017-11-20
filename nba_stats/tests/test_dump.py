import unittest
from unittest import mock

try:
    # For Py2, this version of StringIO is untested
    from StringIO import StringIO
except ImportError:
    # For Py3
    from io import StringIO

import numpy as np
import pandas as pd

import utils
from dump import S3Dumper

SQL_TABLE_READS = 109
S3_UPLOAD_CALLS = SQL_TABLE_READS * 3

@mock.patch("dump.pd")
class TestDump(unittest.TestCase):
    test_df = pd.DataFrame(np.random.randint(0,100,size=(10, 4)))

    @classmethod
    def setUp(self):
        """
        These tests require a read-only database connection
        """
        self.s3 = mock.MagicMock()
        self.s3.put_object = mock.MagicMock()

        engine = utils.get_db()
        self.conn = engine.connect()

    def test_read_sql(self, mock_pd):
        """
        Check that the dumper reads from SQL the right amount of times (109)
        """
        mock_pd.read_sql_table = mock.MagicMock(return_value=self.test_df)

        dumper = S3Dumper()
        dumper.dump(self.conn, self.s3)

        self.assertEqual(SQL_TABLE_READS, mock_pd.read_sql_table.call_count)


    def test_dump_upload_s3(self, mock_pd):
        """
        Check that the dumper uploads to S3 the right amount of times (327)
        """
        mock_pd.read_sql_table = mock.MagicMock(return_value=self.test_df)

        dumper = S3Dumper()
        dumper.dump(self.conn, self.s3)

        self.assertEqual(S3_UPLOAD_CALLS, self.s3.put_object.call_count)
