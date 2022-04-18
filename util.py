import pandas as pd
import numpy as np
import random

#################### HELPER FUNCTIONS ####################

RANDOM_SEED = 0
random.seed(RANDOM_SEED)
np.random.seed(RANDOM_SEED)

def all_variable_names_in_df(variable_names, df):
    """
    Input:
        - variable_names: list of string, of all the variable
                        names to check whether they're in the df or nah
        - df: Pandas DataFrame

    Output:
        - boolean: True if all the variable names are the columns of df,
                    False if not
    """
    columns = set(df.columns)
    for variable_name in variable_names:
        if variable_name not in columns:
            return False
    return True


def train_test_split(df, train_pct=0.8):
    """
    Input:
        - df: Pandas DataFrame
        - train_pct: optional, float
    Output:
        - train dataframe: Pandas DataFrame
        - test dataframe: Pandas DataFrame
    """
    random.seed(RANDOM_SEED)
    np.random.seed(RANDOM_SEED)
    msk = np.random.rand(len(df)) < train_pct
    return df[msk], df[~msk]


def drop_incomplete_rows(df):
    """
    Input:
        - df: Pandas DataFrame
    Output:
        - a Pandas DataFrame where all rows no longer
        contain null values or empty strings
    """
    columns = df.columns
    def row_complete(row):
        for col in columns:
            val = row[col]
            nan = pd.isnull(val)
            str_empty = type(val) == str and val.strip() == ""
            if nan or str_empty:
                return False
        return True
    return df[df.apply(lambda x: row_complete(x), axis=1)]
    


def timestr_to_seconds(time):
    """
    Input:
        - time: str, example: "0:12:11"
    Output:
        - secs: int, number of seconds
    """
    hour, minute, second = time.split(':')
    return int(hour)*3600 + int(minute)*60 + int(second)