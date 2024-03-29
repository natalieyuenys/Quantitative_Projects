import pandas as pd
import numpy as np
import yfinance as yf
import plotly.graph_objects as go
from plotly.subplots import make_subplots

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

def generate_signal(x, overbought, oversold):

    if (min(x['Open'], x['Close']) < x['sma_200']) & (x['rsi']<overbought):
        return 1
    elif (max(x['Open'], x['Close']) > x['sma_50']) & (x['rsi']>oversold): 
        return -1
    else:
        return 0

def update_position(position, signal):

    if position!=0:
        return signal
    else:
        return 0
    
def get_df_trade_position(df,col_position, col_signal):
    
    df = df[df[col_signal]!=0]
    
    df[col_position] = df[col_signal].diff()

    df[col_position] = df.apply(lambda row: update_position(row[col_position],row[col_signal]), axis=1)
    
    df = df[df[col_position]!=0]
    
    return df

def pointpos_pattern(x):

    if x['position']==-1:
        return x['High']+3
    elif x['position']==1:
        return x['Low']-3
    else:
        return np.nan

def generate_chart(df):

    fig = make_subplots(rows=3, cols=1, shared_xaxes=True, row_heights=[0.6, 0.2, 0.2])

    candlestick =   go.Candlestick(x=df.index,
                    open=df['Open'],
                    high=df['High'],
                    low=df['Low'],
                    close=df['Close'])

    sma_50 = go.Scatter(x=df.index, y=df['sma_50'], mode='lines', name='sma_50', line=dict(color="MediumPurple"))
    sma100 = go.Scatter(x=df.index, y=df['sma_100'], mode='lines', name='sma_100', line=dict(color="orange"))
    sma150 = go.Scatter(x=df.index, y=df['sma_150'], mode='lines', name='sma_150', line=dict(color="pink"))
    sma200 = go.Scatter(x=df.index, y=df['sma_200'], mode='lines', name='sma_200', line=dict(color="LightGreen"))
    bb_upper = go.Scatter(x=df.index, y=df['bb_upper'], mode='lines', name='Upper Bollinger Band', line=dict(color="blue"))
    bb_lower = go.Scatter(x=df.index, y=df['bb_lower'], mode='lines', name='Lower Bollinger Band', line=dict(color='blue'))

    
    signal_sell =  go.Scatter(x=df[df['position']==1].index, y=df[df['position']==1]['pointpos_pattern'], mode='markers', name='signal', marker=dict(color="orange",symbol='arrow-bar-up'))
    signal_buy =  go.Scatter(x=df[df['position']==-1].index, y=df[df['position']==-1]['pointpos_pattern'], mode='markers', name='signal', marker=dict(color="orange",symbol='arrow-bar-down'))



    fig.add_trace(candlestick, row=1, col=1)
    fig.add_trace(sma_50, row=1, col=1)
    fig.add_trace(sma100, row=1, col=1)
    fig.add_trace(sma150, row=1, col=1)
    fig.add_trace(sma200, row=1, col=1)
    fig.add_trace(bb_upper, row=1, col=1)
    fig.add_trace(bb_lower, row=1, col=1)

    fig.add_trace(signal_sell, row=2, col=1)
    fig.add_trace(signal_buy, row=2, col=1)

    rsi = go.Scatter(x=df.index, y=df['rsi'], mode='lines', name='rsi', line=dict(color='grey'))
    rsi_overbought = go.Scatter(x=df.index, y=[80]*len(df), mode='lines', name='rsi_overbought', line=dict(color='blue'))
    rsi_oversold = go.Scatter(x=df.index, y=[20]*len(df), mode='lines', name='rsi_oversold', line=dict(color='blue'))

    fig.add_trace(rsi, row=3, col=1)
    fig.add_trace(rsi_overbought, row=3, col=1)
    fig.add_trace(rsi_oversold, row=3, col=1)

    # fig.add_scatter(x=df.index, y=df['rsi'], mode='lines', name='rsi', line=dict(color="orange"))
    # fig.add_scatter(x=df.index, y=df['pointpos'], mode="markers",
    #                 marker=dict(size=5, color="MediumPurple", symbol='circle'),
    #                 name="pivot")

    fig.update_layout(xaxis_rangeslider_visible=False)

    fig.show()
