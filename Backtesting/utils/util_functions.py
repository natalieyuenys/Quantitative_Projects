import pandas as pd
import utils.util_functions as uf

import yfinance as yf

import datetime
from dateutil.relativedelta import relativedelta


def getdata(sym, close):
    
    today = datetime.datetime.now()
    df = yf.download(sym, start=datetime.datetime(today.year-2,today.month, 1),
                                    end=datetime.datetime(today.year, today.month, 1)) 
    pd.set_option('display.max_columns', None)

    df = df[['Open','High','Low',close,'Volume']]
    df = df.reset_index().rename(columns={'index':'Date'})
    df['ticker'] =sym

    return df

def get_backtest_data(df, n_months):

    today = datetime.datetime.now()
    current_month = datetime.datetime(today.year,today.month, 1)
    past_n_months = current_month-relativedelta(months=n_months)

    df = df[(df['Date']>=past_n_months)&(df['Date']<current_month)]

    print("Backtesting on previous {} months".format(n_months))

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