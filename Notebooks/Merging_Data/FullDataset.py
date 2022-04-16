import pandas as pd
import numpy as np
import random
import WranglerFunctions as wf

from datetime import datetime
from datetime import timedelta


def mergeToOne(df1, df2):
    merge = (df1.merge(df2,how='left', left_on= 'Date', right_on = 'Date'))
    return merge

def RenameDateTimeColumnName(df):
    df_dates = df.select_dtypes(include='datetime')
    datetime_columns = df_dates.columns

    if len(datetime_columns) == 0:
        df.reset_index(inplace=True)
        df_dates = df.select_dtypes(include='datetime')
        datetime_columns = df_dates.columns

    df_date_column_name = datetime_columns[0]

    if df_date_column_name != 'Date':
        df.rename(columns = {df_date_column_name : 'Date'}, inplace = True)

def fillInNanValues(df):
    #return df.bfill().ffill()
    return df.ffill().bfill()
def createDailyDataframe(start_date, end_date):
    df_dates = pd.date_range(start = start_date, end = end_date)
    df = df_dates.to_frame(name = 'Date')
    df.index = range(len(df))
    return df

def addNewDataframe(total_df, new_df, new_df_name):
    if new_df_name != "":
        new_df = new_df.add_prefix(new_df_name + "_") #adds df name as prefix to all its columns
    RenameDateTimeColumnName(new_df) #finds and renames date column to the same as the whole table
    total_df = mergeToOne(total_df, new_df)
    return total_df

def InitialDates():
    initial_start_date = '01/01/1990'
    initial_end_date   = '12/04/2022'
    return createDailyDataframe(initial_start_date, initial_end_date)

def AddingCommodities(whole_df):
    CL1_COMB_Comodity  =  wf.format_commodity_data_of_form_DATES_AND_PX_LAST('CL1_COMB_Comodity')     #Crude Oil
    whole_df            = addNewDataframe(whole_df, CL1_COMB_Comodity, "CL1_COMB_Comodity")

    LMAHDS03_LME_Comdty  =  wf.format_commodity_data_of_form_DATES_AND_PX_LAST('LMAHDS03_LME_Comdty') #Aluminium
    whole_df            = addNewDataframe(whole_df, LMAHDS03_LME_Comdty, "LMAHDS03_LME_Comdty")

    LMPBDS03_LME_Comdty  =  wf.format_commodity_data_of_form_DATES_AND_PX_LAST('LMPBDS03_LME_Comdty') #Lead
    whole_df            = addNewDataframe(whole_df, LMPBDS03_LME_Comdty, "LMPBDS03_LME_Comdty")

    LMSNDS03_LME_Comdty  =  wf.format_commodity_data_of_form_DATES_AND_PX_LAST('LMSNDS03_LME_Comdty') #Tin
    whole_df            = addNewDataframe(whole_df, LMSNDS03_LME_Comdty, "LMSNDS03_LME_Comdty")

    LMCADS03_LME_Comdty  =  wf.format_commodity_data_of_form_DATES_AND_PX_LAST('LMCADS03_LME_Comdty') #Copper
    whole_df            = addNewDataframe(whole_df, LMCADS03_LME_Comdty, "LMCADS03_LME_Comdty")

    LMNIDS03_LME_Comdty  =  wf.format_commodity_data_of_form_DATES_AND_PX_LAST('LMNIDS03_LME_Comdty') #Nickel
    whole_df            = addNewDataframe(whole_df, LMNIDS03_LME_Comdty, "LMNIDS03_LME_Comdty")

    LMCODY_LME_Comdty  =  wf.format_commodity_data_of_form_DATES_AND_PX_LAST('LMCODY_LME_Comdty')     #Cobalt -> Only goes to 05/31/2010
    whole_df            = addNewDataframe(whole_df, LMCODY_LME_Comdty, "LMCODY_LME_Comdty")

    LTBMPRIN_Index  =  wf.format_commodity_data_of_form_DATES_AND_PX_LAST('LTBMPRIN_Index')           #Lithium -> Only goes to 2009
    whole_df            = addNewDataframe(whole_df, LTBMPRIN_Index, "LTBMPRIN_Index")
    return whole_df

def AddingInflation(whole_df):
    raw_inflation = pd.read_csv('../../Notebooks/Datasets/Economic_dataset/Inflation.csv')
    inflation     = wf.Unemployment_Wrangler(raw_inflation)
    whole_df      = addNewDataframe(whole_df, inflation, "")
    return whole_df

def AddingUnemployment(whole_df):
    raw_unemployment = pd.read_csv('../../Notebooks/Datasets/Economic_dataset/Unemployment.csv')
    unemployment     = wf.Unemployment_Wrangler(raw_unemployment)
    whole_df         = addNewDataframe(whole_df, unemployment, "")
    return whole_df

def renameMultiIndex(df):
    multiIndex = df.columns
    newIndex   = []
    for e in multiIndex:
        string = e[0] + " " + e[1]
        newIndex.append(string)
    df.columns = newIndex

def AddingSP500Index(whole_df):
    #S&P500 index
    original_SPX500 = pd.read_csv('../../Notebooks/Datasets/Financial_dataset/SPX500.csv')
    SPX500 = wf.SPX500_Wrangler(original_SPX500)
    SPX500_important = SPX500[[('SPX500 Index',   'PX_LAST'), ('SPX500 Index', 'PX_VOLUME')]]
    renameMultiIndex(SPX500_important)
    whole_df         = addNewDataframe(whole_df, SPX500_important, "")
    return whole_df

def AddingFTSE350Index(whole_df):
    #FTSE 350 Index
    F3METL_original = pd.read_csv('../Datasets/Financial_dataset/F3METL.csv', index_col = False)
    F3METL          = wf.F3METL_Wrangler(F3METL_original)
    F3METL_important  = F3METL[['PX_LAST', 'PX_VOLUME']]
    whole_df        = addNewDataframe(whole_df, F3METL_important, "F3METL")
    return whole_df

def AddingGUKG10(whole_df):
    original_data_GUKG10 = pd.read_csv('../../Notebooks/Datasets/Financial_dataset/GUKG10.csv')
    GUKG10  = wf.GUKG10_Wrangler(original_data_GUKG10)
    GUKG10_important = GUKG10[[('GUKG10 Index',   'PX_LAST')]]
    renameMultiIndex(GUKG10_important)
    whole_df         = addNewDataframe(whole_df, GUKG10_important, "")
    return whole_df

def AddingBCOMIN(whole_df):
    #BCOMIN
    original_BCOMIN = pd.read_csv('../../Notebooks/Datasets/Financial_dataset/BCOMIN.csv', index_col=False)
    BCOMIN = wf.BCOMIN_Wrangler(original_BCOMIN).set_index('Dates')
    BCOMIN_important = BCOMIN[['PX_LAST']]
    whole_df       = addNewDataframe(whole_df, BCOMIN_important, 'BCOMIN')
    return whole_df

def AddingGDPGrowth(whole_df):
    uk_GDP = pd.read_csv('../Datasets/Geography_dataset/uk_GDP.csv', index_col = False)
    uk_GDP = wf.gdpWrangler(uk_GDP)
    whole_df = addNewDataframe(whole_df, uk_GDP, "UK")

    china_GDP = pd.read_csv('../Datasets/Geography_dataset/chinaGDP.csv', index_col = False)
    china_GDP = wf.gdpWrangler(china_GDP)
    whole_df = addNewDataframe(whole_df, china_GDP, "China")

    japan_GDP = pd.read_csv('../Datasets/Geography_dataset/japan_GDP.csv', index_col = False)
    japan_GDP = wf.gdpWrangler(japan_GDP)
    whole_df = addNewDataframe(whole_df, japan_GDP, "Japan")

    us_GDP = pd.read_csv('../Datasets/Geography_dataset/us_GDP.csv', index_col = False)
    us_GDP = wf.gdpWrangler(us_GDP)
    whole_df = addNewDataframe(whole_df, us_GDP, "USA")
    return whole_df

def AddingShippingCosts(whole_df):
    shippingCosts = pd.read_csv('../Datasets/Shipping_dataset/WCI_Freight_Rate_Composite.csv', index_col = False)
    shippingCosts = wf.ShippingWrangler(shippingCosts)
    whole_df = addNewDataframe(whole_df, shippingCosts, "Shipping costs")
    return whole_df

def ConvertAllColumnsToFloat(df):
    columnsToConvert = df.select_dtypes(exclude='float64')
    columnNames = columnsToConvert.columns
    for name in columnNames:
        if name != "Date":
            df[name] = df[name].astype('float64')
    return df

def getEBITDAUnique(df, companyName):
    earnings_unique = df[companyName]['EBITDA'].drop_duplicates()
    earnings_unique = pd.DataFrame(earnings_unique)
    earnings_unique = earnings_unique.dropna()
    earnings_unique = earnings_unique.reset_index()
    return earnings_unique

def GetFullDatasetForCompany(company):
    whole_df = InitialDates()
    whole_df = AddingCommodities(whole_df)
    whole_df = AddingInflation(whole_df)
    whole_df = AddingUnemployment(whole_df)
    whole_df = AddingSP500Index(whole_df)
    whole_df = AddingFTSE350Index(whole_df)
    whole_df = AddingGUKG10(whole_df)
    whole_df = AddingBCOMIN(whole_df)
    whole_df = AddingGDPGrowth(whole_df)
    whole_df = AddingShippingCosts(whole_df)

    companies_financial_dataset = pd.read_csv('../../Notebooks/Datasets/Financial_dataset/F3METL_Comp.csv', index_col = False)
    companies_financial_dataset = wf.F3Metl_Comp_Wrangler(companies_financial_dataset)

    feature_df = fillInNanValues(whole_df)
    feature_df = ConvertAllColumnsToFloat(feature_df)
    companies_ebitda = getEBITDAUnique(companies_financial_dataset, company)
    RenameDateTimeColumnName(companies_ebitda)

    companies_ebitda_vs_features = addNewDataframe(companies_ebitda, feature_df, "")
    return companies_ebitda_vs_features
