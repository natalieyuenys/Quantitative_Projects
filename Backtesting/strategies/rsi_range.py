import pandas as pd
import numpy as np

import ta

def get_signal(df, close, n_periods, overbought_threshold, oversold_threshold, stop_loss_pct):
    
    print("Executing RSI Range with parameter {}...".format(n_periods))

    df['rsi'] = ta.momentum.rsi(df[close], window=n_periods)
    df.dropna(subset=['rsi'],inplace=True)

    df['Signal'] = 0
    df.loc[df['rsi']>overbought_threshold, 'Signal'] = -1
    df.loc[df['rsi']<oversold_threshold, 'Signal'] = 1

    # Incorporate Stop Loss
    df['price_change'] = df[close].pct_change()

    df.loc[df['price_change']<-stop_loss_pct,'Signal'] = -1

    ''' move the signal of today to tmr, thus, we need to define a shift(1), as the signal buy is based on yesterday'''
    df['Signal'] = df['Signal'].shift(1)


    return df