import pandas as pd
import numpy as np

import ta
from ta.volatility import BollingerBands


def SMA(df, n, close):
    """
    Return simple moving average of `values`, at
    each step taking into account `n` previous values.

    df (pd.DataFrame)
    n (int): Number of previous values
    close (str): Which column to calculate the SMA
    """
    
    return pd.Series(df[close]).rolling(n).mean()

def signal_sma_crossover(data, close, sma_value, stop_loss_pct):  

    #table start
    df =  data.copy()

    for i in sma_value:
        variable_name = 'SMA'+ str(i)
        df[variable_name] = SMA(df,i,close)
    
    short_sma = min(sma_value)
    long_sma = max(sma_value)

    print("Executing SMA CrossOver with SMA{} and SMA{}...".format(short_sma, long_sma))

    short_sma_col = 'SMA{}'.format(short_sma)
    long_sma_col = 'SMA{}'.format(long_sma)

    '''To make sure row arrange in an ascending order'''
    df.sort_values(by = 'Date',inplace=True)
    
    '''Process data by remove Null value in moving average varaible that your want to used for triggered''' 
    df.dropna(subset=[short_sma_col, long_sma_col],inplace=True)

    '''generate as 1 if Adj close is higher than variable you want to test, generate as -1 if Adj close is less than the
    variable you want to test in a signal variable  
    '''
    # create a signal variable
    df['Signal'] = np.nan 
    # trigger a buy only if it is a up trend 
    df.loc[(df[close]>=df[short_sma_col]) &(df[short_sma_col]>=df[long_sma_col]) ,'Signal'] = 1
    
    # just triggered sell as close is less than variable triggered
    df.loc[(df[close]<df[short_sma_col]),'Signal'] = -1
    
    # if close > variable triggered but sma20<= sma 200, let it be do nothing
    df.loc[(df[close]>=df[short_sma_col]) &(df[short_sma_col]<df[long_sma_col]) ,'Signal'] =0

    # Incorporate Stop Loss
    df['price_change'] = df[close].pct_change()

    df.loc[df['price_change']<-stop_loss_pct,'Signal'] = -1
    
    ''' move the signal of today to tmr, thus, we need to define a shift(1), as the signal buy is based on yesterday'''
    df['Signal'] = df['Signal'].shift(1)
    
    return df

def signal_bollinger_bands_range(df, close):

    print("Executing Bollinger Bands Range...")

    # Initialize Bollinger Bands indicator
    indicator_bb = BollingerBands(close=df[close], window=20, window_dev=2)

    # Get Bollinger Bands
    df['bb_upper'] = indicator_bb.bollinger_hband()
    df['bb_middle'] = indicator_bb.bollinger_mavg()
    df['bb_lower'] = indicator_bb.bollinger_lband()

    # Generate buy and sell signals
    df['Signal'] = 0
    df.loc[df[close] < df['bb_lower'], 'Signal'] = 1
    df.loc[df[close] > df['bb_upper'], 'Signal'] = -1

    return df

def signal_rsi_range(df, close, n_periods, overbought_threshold, oversold_threshold, stop_loss_pct):
    
    print("Executing RSI Range with parameter {}...".format(n_periods))

    df['rsi'] = ta.momentum.rsi(df[close], window=n_periods)
    df.dropna(subset=['rsi'],inplace=True)

    df['Signal'] = 0
    df.loc[df['rsi']>overbought_threshold, 'Signal'] = -1
    df.loc[df['rsi']<oversold_threshold, 'Signal'] = 1

    # Incorporate Stop Loss
    df['price_change'] = df[close].pct_change()

    df.loc[df['price_change']<-stop_loss_pct,'Signal'] = -1

    return df

def signal_rsi_crossover(df, close, list_periods, stop_loss_pct):

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
    


    
    

