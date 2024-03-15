import pandas as pd
import numpy as np

def get_number_trades(ticker, df_trades):

    #print("Number of trades on {} = {}".format(ticker, len(df_trades)))

    return float(len(df_trades))

def get_trade_return(ticker, df_trades):

    #print("Strategy return on {} = {}".format(ticker, df_trades['return'].sum()))

    return round(df_trades['return'].sum(),0)

def get_avg_rate_return(ticker, df_trades):

    #print("Average rate of return on {} = {}".format(ticker, pd.Series(df_trades['rate of return']).mean()))
    return round(pd.Series(df_trades['rate of return']).mean(),2)

def get_best_trade_return(ticker, df_trades):

    #print("Best trade return on {} = {}".format(ticker, pd.Series(df_trades['rate of return']).max()))

    return round(pd.Series(df_trades['rate of return']).max(),2)

def get_worst_trade_return(ticker, df_trades):

    #print("Worst trade return on {} = {}".format(ticker, pd.Series(df_trades['rate of return']).min()))

    return round(pd.Series(df_trades['rate of return']).min(),2)

def get_win_rate(ticker, df_trades):

    win_trades = df_trades[df_trades['return']>0]
    win_rate = round(len(win_trades)/len(df_trades),1)
    
    #print("Win rate on {} = {}%".format(ticker, win_rate))

    return win_rate

def get_win_loss_ratio(ticker, df_trades):

    win_trades = df_trades[df_trades['return']>0]
    loss_trades = df_trades[df_trades['return']<0]

    win_loss_ratio = round((len(win_trades)/len(loss_trades)),2)
    #print("Win-Loss ratio on {} = {}".format(ticker, win_loss_ratio))

    return win_loss_ratio

def get_sharpe_ratio(ticker, df_trades, risk_free_rate):
    
    average_return = np.mean(df_trades['return'])
    return_std = np.std(df_trades['return'])
    
    sharpe_ratio = round((average_return - risk_free_rate) / return_std,2)  

    #print("Sharpe Ratio on {} = {}%".format(ticker, sharpe_ratio))

    return sharpe_ratio