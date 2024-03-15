import pandas as pd

import yfinance as yf

import datetime


def getdata(sym, close):
    
    today = datetime.datetime.now()
    df = yf.download(sym, start=datetime.datetime(today.year-2,today.month, 1),
                                    end=datetime.datetime(today.year, today.month, 1)) 
    pd.set_option('display.max_columns', None)

    df = df[['Open','High','Low',close,'Volume']]
    df = df.reset_index().rename(columns={'index':'Date'})
    df['ticker'] =sym

    return df