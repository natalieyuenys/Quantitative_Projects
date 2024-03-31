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


def get_signal(df, close, sma_value):

    # Calculate MACD
    df['exp12'] = df[close].ewm(span=12, adjust=False).mean()
    df['exp26'] = df[close].ewm(span=26, adjust=False).mean()
    df['macd'] = df['exp12'] - df['exp26']
    df['signal_line'] = df['macd'].ewm(span=9, adjust=False).mean()
    df['histogram'] = df['macd'] - df['signal_line']

    for i in sma_value:
        variable_name = 'SMA'+ str(i)
        df[variable_name] = SMA(df,i,close)
        
    print(f"Executing MACD Crossover ..., i.e. buy when price above {variable_name} and MACD crossed above Signal line below 0, sell when price below {variable_name} or crossed below Signal line above 0")

    df['Signal'] = 0
    df.loc[(df[['Open', close]].min(axis=1) > df[variable_name]) & (df['macd']>=df['signal_line']) & (df['macd']<0),'Signal'] = 1
    df.loc[(df[['Open', close]].min(axis=1) > df[variable_name]) & (df['macd']<=df['signal_line']) & (df['macd']>0),'Signal'] = -1
    df.loc[(df[['Open', close]].min(axis=1) < df[variable_name]),'Signal'] = -1
    
    return df