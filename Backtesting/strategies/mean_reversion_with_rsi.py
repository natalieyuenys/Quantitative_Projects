import pandas as pd
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


def get_signal(df, close, sma_value, rsi_periods, oversold, overbought):

    df['rsi'] = ta.momentum.rsi(df[close], window=rsi_periods)

    for i in sma_value:
            variable_name = 'SMA'+ str(i)
            df[variable_name] = SMA(df,i,close)
        
    short_sma = min(sma_value)
    long_sma = max(sma_value)

    short_sma_col = 'SMA{}'.format(short_sma)
    long_sma_col = 'SMA{}'.format(long_sma)

    print(f"Executing Mean Reversion ..., i.e. buy when below sma_{long_sma} and rsi_{rsi_periods} below {oversold}, sell when above sma_{short_sma} and rsi_{rsi_periods} above {overbought}")

    df['Signal'] = 0
    df.loc[(df[['Open', close]].min(axis=1) < df[long_sma_col]) & (df['rsi']<oversold),'Signal'] = 1
    df.loc[(df[['Open', close]].max(axis=1) > df[short_sma_col]) & (df['rsi']>overbought),'Signal'] = -1
    
    ''' move the signal of today to tmr, thus, we need to define a shift(1), as the signal buy is based on yesterday'''
    df['Signal'] = df['Signal'].shift(1)

    return df