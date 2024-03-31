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

    # Calculate MACD
    df['exp12'] = df['Close'].ewm(span=12, adjust=False).mean()
    df['exp26'] = df['Close'].ewm(span=26, adjust=False).mean()
    df['macd'] = df['exp12'] - df['exp26']
    df['signal_line'] = df['macd'].ewm(span=9, adjust=False).mean()
    df['histogram'] = df['macd'] - df['signal_line']    
    
    df.dropna(subset=[sma_var_name],inplace=True)

    return df

def generate_signal(x, sma_var_name):

    if (min(x['Open'], x['Close']) > x[sma_var_name]) & (x['macd']>=x['signal_line']) & (x['macd']<0):
        return 1
    elif (min(x['Open'], x['Close']) > x[sma_var_name]) & (x['macd']<=x['signal_line']) & (x['macd']>0): 
        return -1
    elif (min(x['Open'], x['Close']) < x[sma_var_name]):
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

    colors = ['green' if val > 0 else 'red' for val in df['histogram']]

    sma_200 = go.Scatter(x=df.index, y=df['sma_200'], mode='lines', name='SMA200', line=dict(color="orange"))
    macd = go.Scatter(x=df.index, y=df['macd'], mode='lines', name='MACD', line=dict(color="blue"))
    signal = go.Scatter(x=df.index, y=df['signal_line'], mode='lines', name='signal', line=dict(color="orange"))
    histogram = go.Bar(x=df.index, y=df['histogram'], name='Histogram', marker=dict(color=colors))
    signal_sell =  go.Scatter(x=df[df['position']==1].index, y=df[df['position']==1]['pointpos_pattern'], mode='markers', name='signal', marker=dict(color="orange",symbol='arrow-bar-up'))
    signal_buy =  go.Scatter(x=df[df['position']==-1].index, y=df[df['position']==-1]['pointpos_pattern'], mode='markers', name='signal', marker=dict(color="orange",symbol='arrow-bar-down'))

    fig.add_trace(candlestick, row=1, col=1)
    fig.add_trace(sma_200, row=1, col=1)

    fig.add_trace(macd, row=2, col=1)
    fig.add_trace(signal, row=2, col=1)
    fig.add_trace(histogram, row=2, col=1)

    fig.add_trace(signal_sell, row=3, col=1)
    fig.add_trace(signal_buy, row=3, col=1)

    fig.update_layout(xaxis_rangeslider_visible=False)

    fig.show()
