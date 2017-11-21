import unittest
from unittest import mock
import string
import random
from os import path
import json

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


SQL_TABLE_READS = 24
S3_UPLOAD_CALLS = SQL_TABLE_READS * 3


def random_string(size=6, chars=string.ascii_uppercase + string.ascii_lowercase):
    return ''.join(random.choice(chars) for _ in range(size))


class FakeInspector(object):
    def __init__(self, conn):
        pass

    def get_table_names(self):
        return iter([random_string() for _ in range(SQL_TABLE_READS)])


@mock.patch("dump.inspect", new=FakeInspector)
@mock.patch("dump.pd")
class TestDump(unittest.TestCase):

    @classmethod
    def setUp(self):
        self.test_df = pd.DataFrame(np.random.randint(0, 100, size=(10, 4)))

        self.s3 = mock.MagicMock()
        self.s3.put_object = mock.MagicMock()

    def test_read_sql(self, mock_pd):
        """
        Check that the dumper reads from SQL the right amount of times
        """
        mock_pd.read_sql_table = mock.MagicMock(return_value=self.test_df)

        dumper = S3Dumper()
        dumper.dump("is normally a sqlalchemy conn", self.s3)

        self.assertEqual(SQL_TABLE_READS, mock_pd.read_sql_table.call_count)

    def test_dump_upload_s3(self, mock_pd):
        """
        Check that the dumper uploads to S3 the right amount of times
        """
        mock_pd.read_sql_table = mock.MagicMock(return_value=self.test_df)

        dumper = S3Dumper()
        dumper.dump("is normally a sqlalchemy conn", self.s3)

        self.assertEqual(S3_UPLOAD_CALLS, self.s3.put_object.call_count)

    def test_s3_put_args(self, mock_pd):
        """
        Check calls to `s3.put_object` use right content-type for the given
        file extension (in the key arg)
        """
        mock_pd.read_sql_table = mock.MagicMock(return_value=self.test_df)

        dumper = S3Dumper()
        dumper.dump("is normally a sqlalchemy conn", self.s3)

        for call in self.s3.put_object.mock_calls:
            args = call[2]
            f_root, f_ext = path.splitext(args["Key"])
            if f_ext == ".json":
                # json.loads will throw an exception if the json cannot be parsed
                throwaway = json.loads(args["Body"])
                content_type = "text/plain"
            elif f_ext == ".csv":
                content_type = "text/plain"
            elif f_ext == ".html":
                content_type = "text/html"
            else:
                raise self.failureException("Argument error on %s" % str(call))
            self.assertEqual(args["ContentType"], content_type)
