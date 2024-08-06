import pandas as pd
import utils.util_functions as uf

import yfinance as yf

import datetime
from dateutil.relativedelta import relativedelta


def getdata(sym, close, n_days, frequency):
    
    today = datetime.datetime.now()
    past_n_days = today-relativedelta(days=n_days)

    print("Backtesting on previous {} days".format(n_days))
    
    df = yf.download(sym, start=past_n_days, end=today, interval=frequency) 
    pd.set_option('display.max_columns', None)

    df = df[['Open','High','Low',close,'Volume']]
    df = df.reset_index().rename(columns={'index':'Date'})
    df['ticker'] =sym

    return df

def update_position(position, signal):

    if position!=0:
        return signal
    else:
        return position
    
def get_df_trade_position(df,col_position, col_signal):
    
    df = df[df[col_signal]!=0]
    
    df[col_position] = df[col_signal].diff()

    df[col_position] = df.apply(lambda row: uf.update_position(row[col_position],row[col_signal]), axis=1)
    
    return df

def get_df_trade_return(df, col_position):
    
    df = df[df[col_position]!=0]

    # Count from first purchase
    df['return'] = df['Previous_day_close'].diff()
    df['rate of return'] = df['Previous_day_close'].pct_change()

    return df[df[col_position]==df.iloc[1][col_position]]