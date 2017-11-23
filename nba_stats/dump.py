import logging

import pandas as pd
from datetime import date

try:
    # For Py2, this version of StringIO is untested
    from StringIO import StringIO
except ImportError:
    # For Py3
    from io import StringIO

import boto3
from sqlalchemy import inspect

import utils

# For debugging
from pprint import pprint
import traceback
import sys
import pdb

DEBUG = True

SEASON = "1718"
DATE_FORMAT = "%Y_%m_%d"

logger = logging.getLogger(__name__)

class S3Dumper(object):

    def __init__(self):
        pass

    @staticmethod
    def dump(conn, s3):
        logger.info("Begin S3 dump")
        inspector = inspect(conn)

        for table_name in inspector.get_table_names():
            logger.info("Dumping table {} to S3".format(table_name))

            si_csv = StringIO()
            si_json = StringIO()
            si_html = StringIO()

            df = pd.read_sql_table(table_name, conn)
            df.to_csv(si_csv)
            df.to_json(si_json)
            df.to_html(si_html)

            for ext, si in zip(
                ["csv", "json", "html"],
                [si_csv, si_json, si_html]):

                pathname = "stats/nba/{}/{}/{}.{}".format(
                    SEASON,
                    "latest",
                    table_name,
                    ext)

                content_type = "text/html" if ext == "html" else "text/plain"

                s3.put_object(
                        Body=si.getvalue(),
                        Bucket='no-pushes',
                        ContentType=content_type,
                        Key=pathname)
        logger.debug("Finished S3 dump")


# def main():
#     engine = utils.get_db()
#     conn = engine.connect()

#     s3 = boto3.client('s3',
#                       aws_access_key_id=config.AWS_ACCESS_KEY_ID,
#                       aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY)

#     S3Dumper.dump(conn, s3)

# if __name__ == "__main__":
#     try:
#         main()
#     except Exception as exc:
#         if DEBUG:
#             type, value, tb = sys.exc_info()
#             traceback.print_exc()
#             pdb.post_mortem(tb)
#         else:
#             raise exc
