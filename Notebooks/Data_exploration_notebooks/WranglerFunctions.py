import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter

def format_date(df, column_name, format_string):
    err = 0
    for i in range(len(df)):
        try:
            df.loc[i, column_name] = pd.to_datetime(df[column_name][i], format = format_string)
        except ValueError:
            err += 1
    return err

def Inflation_Unemployment_Wrangler(df):
    date_err = format_date(df, 'Date', '%d/%m/%Y')
    df = df.iloc[::-1]
    df = df.reset_index(drop = True)
    return df, date_err

def F3Metl_Comp_Wrangler(data):
    # Delete the first row (full of null values)
    df = data.drop(labels=0)

    # Delete the index column since the date is the index
    df.rename(columns={'Unnamed: 0': 'Dates'}, inplace=True)
    df.set_index('Dates', inplace=True)


    # Rename the column headers
    df = df.drop(labels='Dates')
    df.columns = pd.MultiIndex.from_product([['RIO LN Equity', 'GLEN LN Equity', 'AAL LN Equity', 'ANTO LN Equity', 'EVR LN Equity', 'BHP LN Equity'], ['PX_OPEN', 'PX_HIGH', 'PX_LOW', 'PX_LAST', 'PX_VOLUME', 'EBITDA','PE_RATIO']])

    # Delete rows without dates
    df = df.drop(labels='#NAME?')

    # Reformat dates
    df.index = pd.to_datetime(df.index, format='%d/%m/%Y')

    # Drop all BHP LN Equity data as it is incomplete
    # However, the EBITDA data might be useful
    # df.drop(columns= [('BHP LN Equity', y) for y in ['PX_OPEN', 'PX_HIGH', 'PX_LOW', 'PX_LAST', 'PX_VOLUME', 'EBITDA','PE_RATIO']], inplace=True)

    # Change numbers to floats/ints (fields with NaN values are floats by default)
    df = df.apply(pd.to_numeric)
    return df

def CostsWrangler(df, start_str):
    #Setting columns as the dates
    df.columns = df.loc[3].values
    #Getting rid of spaces in front of string
    df['12 Months Ending'] = df['12 Months Ending'].str.strip()
    #Removing nan columns
    df = df.loc[:, df.columns.notna()]
    
    # Removing unneccessary rows
    df = df.drop([0, 1, 2, 3, len(df) - 1], axis = 0)
    df = df.reset_index(drop = True)
    
    # Get revenue index
    rev_idx = df['12 Months Ending'][df['12 Months Ending'] == start_str].index[0]
    
    # Some float values have commas separating thousands - creates problems when converting to float
    df = df.replace(',','', regex=True)
    
    # Replace the + and - characters
    df = df.replace('\+ ','', regex=True)
    df = df.replace('- ','', regex=True)
    
    # Putting dates as rows now
    df = df.T
    
    # Columns as countries
    df.columns = df.loc['12 Months Ending']
    
    # Only selecting relevant columns
    df = df.iloc[:, rev_idx:]
    
    df = df.drop(['12 Months Ending'], axis = 0)
    
    # Converting values to float
#     for column in df.columns:
    # df.columns
    df['Operating Expenses'] = df['Operating Expenses'].astype(float)    
                
    # Missing data as 0.0 - not 100% necessary
    df = df.replace(np.nan, 0.0)
    
    # Date as datetime format
    df = df.reset_index()
    df = df.rename(columns = {"index" : "Date"})
    
    print(format_date(df, 'Date', '%m/%d/%Y'))
    df.index = df['Date']
    
    df = df.drop('Date', axis = 1)
    
#     Only using data from 2010    
    df = df[(df.index > '2010-01-01') & (df.index <'2022-01-01')]
    
    return df
