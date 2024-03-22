import pandas as pd
import yfinance as yf

def SMA(df, n, Close):
    return pd.Series(df[Close]).rolling(n).mean()

def getdata(sym, sma_value, close, start_date, end_date):
    
    df=yf.download(sym, start=start_date, end=end_date)
    pd.set_option('display.max_columns', None)

    df = df[['Open','High','Low',close,'Volume']]
    df = df.reset_index().rename(columns={'index':'Date'})
    df['ticker'] = sym

    # Moving Averages
    for i in sma_value:
        sma_var_name = 'sma_' + str(i)
        df[sma_var_name] = SMA(df, i, close)

    return df
    