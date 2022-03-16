import pandas as pd

def format_date(df, column_name, format_string):
    err = 0
    for i in range(len(df)):
        try:
            df[column_name][i] = pd.to_datetime(df[column_name][i], format = format_string)
        except ValueError:
            err += 1
    return err
