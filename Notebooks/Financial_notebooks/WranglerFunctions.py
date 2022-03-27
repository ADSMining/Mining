import pandas as pd

def format_date(df, column_name, format_string):
    err = 0
    for i in range(len(df)):
        try:
            df[column_name][i] = pd.to_datetime(df[column_name][i], format = format_string)
        except ValueError:
            err += 1
    return err

def Inflation_Wrangler(df):
    date_err = format_date(df, 'Date', '%d/%m/%Y')
    df = df.iloc[::-1]
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
  

def SPX500_Wrangler(data):
    # Delete the first row (full of null values)
    df = data.drop(labels=0)

    # Delete the index column since the date is the index
    df.rename(columns={'Unnamed: 0': 'Dates'}, inplace=True)
    df.set_index('Dates', inplace=True)


    # Rename the column headers 
    df = df.drop(labels='Dates')
    df = df.drop(labels='#NAME?')
    df.columns = pd.MultiIndex.from_product([['SPX500 Index'], ['PX_OPEN', 'PX_HIGH', 'PX_LOW', 'PX_LAST', 'PX_VOLUME']])


    # Reformat dates
    df.index = pd.to_datetime(df.index, format='%d/%m/%Y')


    
    return df

    # Change numbers to floats/ints (fields with NaN values are floats by default)
    

def F3METL_Wrangler(original_data):
# Delete the first row 
    df = original_data.drop(labels=1)

    # Rename the column headers 
    new_header = df.iloc[0]
    df = df[1:]
    df.columns = new_header

    # Delete the index column since the date is the index
    df.set_index('Dates', inplace=True)

    # Reformat dates
    df.index = pd.to_datetime(df.index, format='%d/%m/%Y')

    # Change numbers to floats/ints (fields with NaN values are floats by default)
    df = df.apply(pd.to_numeric)

    # Drop the general earning index
    df.drop('INDX_GENERAL_EARN', axis=1, inplace=True)

    return df
