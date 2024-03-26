import pandas as pd
import numpy as np

import ta


def get_signal(df, close, list_periods, stop_loss_pct):

    for n_periods in list_periods:
        variable_name = 'rsi'+ str(n_periods)
        df[variable_name] = ta.momentum.rsi(df[close], window=n_periods)
    
    short_rsi = min(list_periods)
    long_rsi = max(list_periods)

    print("Executing RSI CrossOver with parameter ({},{})...".format(short_rsi,long_rsi))

    short_rsi_col = 'rsi{}'.format(short_rsi)
    long_rsi_col = 'rsi{}'.format(long_rsi)

    df.dropna(subset=[short_rsi_col,long_rsi_col],inplace=True)

    # create a signal variable
    df['Signal'] = 0

    df.loc[df[short_rsi_col]>=df[long_rsi_col],'Signal'] = -1
    df.loc[df[short_rsi_col]<df[long_rsi_col],'Signal'] = 1
    
    # Incorporate Stop Loss
    df['price_change'] = df[close].pct_change()

    df.loc[df['price_change']<-stop_loss_pct,'Signal'] = -1

    ''' move the signal of today to tmr, thus, we need to define a shift(1), as the signal buy is based on yesterday'''
    df['Signal'] = df['Signal'].shift(1)

    return df