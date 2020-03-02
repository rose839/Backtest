import os
import pandas as pd

def assert_msg(condition, msg):
    if not condition:
        raise Exception(msg)

def read_file(filename):
    filepath = os.path.join(path.dirname(__file__), filename)

    assert_msg(os.path.exists(filepath), "File doesn't exists!")

    # read CSV file
    return pd.read_csv(filepath,
                       index_col=0,
                       parse_dates=True,
                       infer_datetime_format=True)