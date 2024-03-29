import pandas as pd
import numpy as np
import ta

import datetime

import util_functions as uf

sma_value = [50, 100, 150, 200]
close='Close'
list_stock = ['AAPL','TSLA','NVDA','GOOG','META','ADBE','AMZN','MSFT','KO']

today = datetime.datetime.now()
end_date = datetime.datetime(today.year, today.month, today.day-1)
start_date = datetime.datetime(today.year-1, 1, 1)

for sym in list_stock:
    df = uf.getdata(sym, sma_value, close, start_date, end_date)

    df['rsi'] = ta.momentum.rsi(df[close], window=50)
    df.dropna(subset=['sma_50','rsi'],inplace=True)

    df['signal'] = df.apply(lambda row: uf.generate_signal(row, overbought=60, oversold=50), axis=1)
    
    df_trade = uf.get_df_trade_position(df, 'position','signal')

    df = df.merge(df_trade[['Date','position']], how='left', on='Date')

    df['pointpos_pattern'] = df.apply(lambda row: uf.pointpos_pattern(row), axis=1)

    # Calculate Bollinger Bands
    indicator_bb = ta.volatility.BollingerBands(close=df[close], window=20, window_dev=2)

    # Get Bollinger Bands
    df['bb_upper'] = indicator_bb.bollinger_hband()
    df['bb_lower'] = indicator_bb.bollinger_lband()

    uf.generate_chart(df)
        