import warnings
warnings.filterwarnings("ignore")

import pandas as pd

import util_functions as uf
import strategies as s
import backtesting as bt
import visualisation as vs


list_stock = ['AAPL','TSLA','NVDA','GOOG','META','ADBE','AMZN','MSFT','KO']
#list_stock=['META']

risk_free_rate = 2.24

short_sma = 10
long_sma = 200

short_rsi = 7
long_rsi = 14

rsi_range_period = 14

list_strategy = ['sma_crossover','rsi_range','rsi_crossover']

for strategy in list_strategy:

# Create an empty dataframe with column names
    df_analysis_heatmap = pd.DataFrame(
        columns= [
            'Stock',
            'No. of trades', 
            'Trade Return', 
            'Avg Return (%)', 
            'Best Trade (%)', 
            'Worst Trade (%)',
            'Win Rate (%)',
            'Win-Loss Ratio',
            'Sharpe Ratio'
            ]
        )

    df_hyp_test = pd.DataFrame()

    for ticker in list_stock :

        try:
            df_raw = uf.getdata(ticker, close = "Adj Close")
            
            ######### Execute Strategies                            
            if strategy == 'sma_crossover':
                df = s.signal_sma_crossover(df_raw, close='Adj Close', sma_value=[short_sma,long_sma], stop_loss_pct=0.03)
                df_trades, df_heatmap = bt.df_backtesting(df, ticker, risk_free_rate)
                title = 'Performance Metrics for sma_crossover with parameter ({},{})'.format(short_sma, long_sma)
                df_test = pd.DataFrame({ticker:df_trades['rate of return']})

            elif strategy == 'rsi_range':
                df = s.signal_rsi_range(df_raw, n_periods=rsi_range_period, close='Adj Close',overbought_threshold=70, oversold_threshold=30, stop_loss_pct=0.03)
                df_trades, df_heatmap = bt.df_backtesting(df, ticker, risk_free_rate)
                title = 'Performance Metrics for rsi_range with parameter {}'.format(rsi_range_period)
                df_test = pd.DataFrame({ticker:df_trades['rate of return']})

            elif strategy == 'rsi_crossover':            
                df = s.signal_rsi_crossover(df_raw, close="Adj Close", list_periods=[short_rsi,long_rsi], stop_loss_pct=0.03)
                df_trades, df_heatmap =bt.df_backtesting(df, ticker, risk_free_rate)
                title = 'Performance Metrics for rsi_crossover with parameter ({},{})'.format(short_rsi, long_rsi)
                df_test = pd.DataFrame({ticker:df_trades['rate of return']})

        except Exception as e:
            print(f"Error occurred: {e}")
            continue

        df_analysis_heatmap = pd.concat([df_analysis_heatmap, df_heatmap])
        df_hyp_test = pd.concat([df_hyp_test, df_test.reset_index(drop=True)], axis=1)
        
    vs.gen_analysis_heatmap(df_analysis_heatmap, title)
