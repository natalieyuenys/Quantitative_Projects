import pandas as pd

import util_functions as uf
import performance_metrics as pm

def df_backtesting(df, ticker, risk_free_rate):

    global df_trades

    df['Previous_day_close'] = df['Adj Close'].shift(1)

    df_backtest = uf.get_backtest_data(df, 6)

    df_position = uf.get_df_trade_position(df_backtest, 'Position', 'Signal')

    df_trades = uf.get_df_trade_return(df_position, 'Position')

    n_trades = pm.get_number_trades(ticker, df_trades)
    trade_return = pm.get_trade_return(ticker, df_trades)
    avg_return = pm.get_avg_rate_return(ticker, df_trades)
    best_trade = pm.get_best_trade_return(ticker, df_trades)
    worst_trade = pm.get_worst_trade_return(ticker, df_trades)
    win_rate = pm.get_win_rate(ticker, df_trades)
    win_loss_ratio = pm.get_win_loss_ratio(ticker, df_trades)
    sharpe_ratio = pm.get_sharpe_ratio(ticker, df_trades, risk_free_rate)

    df_heatmap = pd.DataFrame({
        'Stock':[ticker],
        'No. of trades': [n_trades], 
        'Trade Return': [trade_return], 
        'Avg Return (%)': [avg_return],
        'Best Trade (%)':[best_trade],
        'Worst Trade (%)':[worst_trade],
        'Win Rate (%)':[win_rate],
        'Win-Loss Ratio':[win_loss_ratio],
        'Sharpe Ratio':[sharpe_ratio]
        })
    
    return df_trades, df_heatmap




