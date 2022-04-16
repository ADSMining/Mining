import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
from datetime import datetime

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

def Unemployment_Wrangler(df):
    df.set_index('Date', inplace=True)
    df.index = pd.to_datetime(df.index, format='%d/%m/%Y')
    df = df.apply(pd.to_numeric)
    return df

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

    df.index = df['Date']

    df = df.drop('Date', axis = 1)

#     Only using data from 2010
    df = df[(df.index > '2010-01-01') & (df.index <'2022-01-01')]

    return df

def ShippingWrangler(df):
    Freight_wrangle1 =df.drop(columns=["Unnamed: 1","Unnamed: 2","Unnamed: 3","Unnamed: 4"])
    Freight_wrangle2 = Freight_wrangle1.T
    Freight_wrangle2.columns =[str(Freight_wrangle2[0][0]), str(Freight_wrangle2[1][0])]
    Freight_wrangle2.drop(["Unnamed: 0"], axis=0,inplace=True)
    Freight_wrangle2['Container Rates (USD per FEU) - WCI Freight Rate Composite'] = Freight_wrangle2['Container Rates (USD per FEU) - WCI Freight Rate Composite'].astype(float)
    Freight_wrangle2 = Freight_wrangle2[Freight_wrangle2['Container Rates (USD per FEU) - WCI Freight Rate Composite']!=0]
    #convert quarters to Data Time format
    Freight_wrangle2["Date"] = pd.to_datetime(Freight_wrangle2["Description"].str.replace(r'(\d+) (Q\d)', r'\1-\2'), errors='coerce')
    Freight_wrangle2 = Freight_wrangle2.drop(columns='Description')
    #Reorder columns
    cols = Freight_wrangle2.columns.tolist()
    cols = cols[1:] + cols[0:1]
    cols
    Freight_wrangle2 = Freight_wrangle2[cols]
    #Reset index
    Freight_wrangle2.set_index(np.arange(1,(len(Freight_wrangle2['Date'])+1)))

    df = Freight_wrangle2
    df.columns = ["Date", "Shipping costs"]

    df = df.iloc[::-1]
    df = df.reset_index(drop = True)

    return df

def format_commodity_data_of_form_DATES_AND_PX_LAST(filename):  #AKA COMMODITY DATASET WRANGLERS
    location = '../../Notebooks/Datasets/Commodity_price_dataset/' + filename + '.csv'
    df = pd.read_csv(location   , index_col=False, names=["Dates", "PX_LAST"])
    df.dropna(inplace=True)
    df.reset_index(drop=True, inplace=True)
    try:
        df["Dates"] = df["Dates"].apply(lambda x: datetime.strptime(x, "%m/%d/%Y"))
    except TypeError:
        df["Dates"] = df["Dates"].apply(lambda x: datetime.strptime(x, "%y/%m/%d"))
    df = df.loc[::-1]
    df.reset_index(drop=True, inplace=True)
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

def GUKG10_Wrangler(data):
    # Delete the first row (full of null values)
    df = data.drop(labels=0)

    # Delete the index column since the date is the index
    df.rename(columns={'Unnamed: 0': 'Dates'}, inplace=True)
    df.set_index('Dates', inplace=True)


    # Rename the column headers
    df = df.drop(labels='Dates')
    df = df.drop(labels='#NAME?')
    df.columns = pd.MultiIndex.from_product([['GUKG10 Index'], ['PX_OPEN', 'PX_HIGH', 'PX_LOW', 'PX_LAST', 'COUPON']])


    # Reformat dates
    df.index = pd.to_datetime(df.index, format='%d/%m/%Y')



    return df


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

def BCOMIN_Wrangler(raw_data):
    clean_data = raw_data.drop(labels=0)

    # Dates should be used to index the dataset
    clean_data.rename(columns={'Unnamed: 0': 'Dates'}, inplace=True)
    #clean_data.set_index('Dates', inplace=True)

    #clean_data = clean_data.drop(labels='Dates')
    clean_data.rename(columns={'BCOMIN Index' : 'PX_OPEN',
                               'Unnamed: 2': 'PX_HIGH',
                               'Unnamed: 3':'PX_LOW',
                               'Unnamed: 4' :'PX_LAST'}, inplace=True)
    clean_data = clean_data.iloc[2: , :] #Remove first 2 error lines
    clean_data.reset_index(drop=True, inplace=True)
    for i in range(len(clean_data)):
        clean_data["Dates"][i] = datetime.strptime(clean_data["Dates"][i], "%d/%m/%Y") #Puts dates into TimeStamp format
    clean_data.set_index('Dates')


    return clean_data


def test_rev_dataset(df):
    for row in df.iterrows():
        print(sum(row[1].values) - row[1].values[0])
        # ADD SMALL MARGIN OF ERROR - SOME DATA IS NOT COMPLETE IN BLOOMBERG - ONLY EVR HAS SOME SMALL ERROR SO FAR
        assert(sum(row[1].values) < row[1].values[0]*2 + 100)
        assert(sum(row[1].values) > row[1].values[0]*2 - 100)

    print("Dataset contains all values for revenue by country")

def Geo_Wrangler(df, start_str, end_str):
    #Setting columns as the dates
    df.columns = df.loc[3].values
    #Getting rid of spaces in front of string
    df['12 Months Ending'] = df['12 Months Ending'].str.strip()
    #Removing nan columns
    df = df.loc[:, df.columns.notna()]

    # Removing unneccessary rows
    df = df.drop([0, 1, 2, 3], axis = 0)
    df = df.reset_index(drop = True)

    # Get revenue index
    rev_idx = df['12 Months Ending'][df['12 Months Ending'] == start_str].index[0]
    end_idx = df['12 Months Ending'][df['12 Months Ending'] == end_str].index[0]

    # Getting rid of ? and replacing as nan
    df = df.replace('?', np.nan)

    # Some float values have commas separating thousands - creates problems when converting to float
    df = df.replace(',','', regex=True)

    # Putting dates as rows now
    df = df.T

    # Columns as countries
    df.columns = df.loc['12 Months Ending']

    # Only selecting relevant columns
    df = df.iloc[:, rev_idx : end_idx]

    df = df.drop(['12 Months Ending'], axis = 0)

    # Converting values to float
    for column in df.columns:
        df[column] = df[column].astype(float)

    # Missing data as 0.0 - not 100% necessary
    df = df.replace(np.nan, 0.0)

    # Date as datetime format
    df = df.reset_index()
    df = df.rename(columns = {"index" : "Date"})

    df.index = df['Date']
    df = df.drop('Date', axis = 1)

    # Only using data from 2010
    df = df[df.index > '2010-01-01']

    # Following if statements are to remove double counting - in Bloomberg we had North America e.g. and then USA and Canada as children
    # When converted to csv both North America is counted and USA and Canada, where as we only want a single instance
    # Also converting Others to correct continent
    if ('North America' in df.columns):
        if 'United States' in df.columns:
            if 'Canada' in df.columns:
                df = df.drop(['North America'], axis = 1)

    if ('Americas' in df.columns):
        if 'USA' in df.columns:
            if 'Mexico' in df.columns:
                df = df.drop(['Americas'], axis = 1)
                index_no = df.columns.get_loc('Mexico')
                column_names = df.columns.values
                column_names[index_no + 1] = "Other countries in Americas"
                df.columns = column_names

    if ('Europe' in df.columns):
        if 'Germany' in df.columns:
            df = df.drop(['Europe'], axis = 1)
            if 'Turkey' in df.columns:
                index_no = df.columns.get_loc('Turkey')
                column_names = df.columns.values
                column_names[index_no + 1] = "Other countries in Europe"
                df.columns = column_names

    if ('Asia' in df.columns):
        if 'Japan' in df.columns:
            df = df.drop(['Asia'], axis = 1)
            if 'Mongolia' in df.columns:
                index_no = df.columns.get_loc('Mongolia')
                column_names = df.columns.values
                column_names[index_no + 1] = "Other countries in Asia"
                df.columns = column_names

    if ('Africa & The Rest Of The World' in df.columns):
        if 'Africa' in df.columns:
            df = df.drop(['Africa & The Rest Of The World'], axis = 1)
            df = df.drop(['Africa'], axis = 1)

            if 'Egypt' in df.columns:
                index_no = df.columns.get_loc('Egypt')
                column_names = df.columns.values
                column_names[index_no + 1] = "Other countries in Africa"
                df.columns = column_names

    if ('CIS' in df.columns):
        if 'CIS (Excluding Russia)' in df.columns:
            if 'Canada' in df.columns:
                df = df.drop(['CIS'], axis = 1)
                df = df.drop(['CIS (Excluding Russia)'], axis = 1)

                if 'Uzbekistan' in df.columns:
                    index_no = df.columns.get_loc('Uzbekistan')
                    column_names = df.columns.values
                    column_names[index_no + 1] = "Other countries in CIS"
                    df.columns = column_names


    if ('Latin America' in df.columns):
        if 'Chile' in df.columns:
            df = df.drop(['Latin America'], axis = 1)

    # Removing columns with no meaningful data
    for column in df.columns:
        unique_values = df[column].unique()
        if len(unique_values) == 1:
            if unique_values[0] == 0.0:
                df = df.drop([column], axis = 1)

    # Removing rows with no data
    for row in df.iterrows():
        unique_values = np.unique(row[1].values)
        if len(unique_values) == 1:
            if unique_values[0] == 0.0:
                df = df.drop([row[0]], axis = 0)


    return df

def gdpWrangler(raw_data):
    df = pd.DataFrame([], columns = ["Date", "GDP growth"])
    df["Date"] = raw_data.loc[7]
    df["GDP growth"] = raw_data.loc[8]
    df = df.reset_index(drop = True)
    df = df.drop([0, 1, 2], axis = 0)
    df = df.iloc[::-1]
    df = df.replace("--", np.nan)
    df = df.dropna()
    df = df.reset_index(drop = True)
    df["GDP growth"] = df['GDP growth'].astype(float)
    df["Date"] = pd.to_datetime(df["Date"].str.replace(r'(Q\d) (\d+)', r'\2-\1'), errors='coerce')

    return df
