import pandas as pd
import numpy as np


def isPivot(df, candle, window):
    """
    function that detects if a candle is a pivot/fractal point
    args: candle index, window before and after candle to test if pivot
    returns: 1 if pivot high, -1 if pivot low
    """
    if candle-window < 0 or candle+window >= len(df):
        return 0
    
    pivotHigh = 1
    pivotLow = -1
    for i in range(candle-window, candle+window+1):
        if df.iloc[candle]['Low'] > df.iloc[i]['Low']:
            pivotLow=0
        if df.iloc[candle]['High'] < df.iloc[i]['High']:
            pivotHigh=0
    if (pivotHigh and pivotLow):
        return 3
    elif pivotHigh:
        return pivotHigh
    elif pivotLow:
        return pivotLow
    else:
        return 0

def detect_breakout(df, candle, backcandles, window, close, zone_width):
    """
    Attention! window should always be greater than the pivot window! to avoid look ahead bias
    """
    if (candle <= (backcandles+window)) or (candle+window+1 >= len(df)):
        return 0
    
    localdf = df.iloc[candle-backcandles-window:candle-window] #window must be greater than pivot window to avoid look ahead bias
    highs = localdf[localdf['isPivot'] == 1]['High'].values
    lows = localdf[localdf['isPivot'] == -1]['Low'].values
    signal = 0
    
    if len(lows)>=1:
        support_condition = True
        mean_low = lows.mean()
        for low in lows:
            if abs(low-mean_low)>zone_width:
                support_condition = False
                break
        if support_condition and (mean_low - df.loc[candle][close])>0:
            signal = -1

    if len(highs)>=1:
        resistance_condition = True
        mean_high = highs.mean()
        for high in highs:
            if abs(high-mean_high)>zone_width:
                resistance_condition = False
                break
        if resistance_condition and (df.loc[candle][close]-mean_high)>0:
            signal = 1
    return signal

def signal_breakout(df, close, backcandles, window, zone_width):

    print("Executing Support-Resistance Breakout...")
    
    df['isPivot'] = df.apply(lambda x: isPivot(df, candle=x.name,window=3), axis=1)
    df['Signal'] = df.apply(lambda row: detect_breakout(df, row.name, backcandles=backcandles, window=window, close=close, zone_width=zone_width), axis=1)
    
    return df