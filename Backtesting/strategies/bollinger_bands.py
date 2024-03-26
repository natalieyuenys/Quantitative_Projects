import pandas as pd
import numpy as np

import ta
from ta.volatility import BollingerBands

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