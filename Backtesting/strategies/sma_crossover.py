import pandas as pd
import numpy as np

import ta


def SMA(df, n, close):
    """
    Return simple moving average of `values`, at
    each step taking into account `n` previous values.

    df (pd.DataFrame)
    n (int): Number of previous values
    close (str): Which column to calculate the SMA
    """
    
    return pd.Series(df[close]).rolling(n).mean()

def get_signal(data, close, sma_value, stop_loss_pct):  

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
