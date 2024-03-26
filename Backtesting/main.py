import warnings
warnings.filterwarnings("ignore")

import pandas as pd

import utils.util_functions as uf
from strategies import sma_crossover
from strategies import rsi_crossover
from strategies import rsi_range
from strategies import support_resistance_breakout
import utils.backtesting as bt
import utils.visualisation as vs


list_stock = ['AAPL','TSLA','NVDA','GOOG','META','ADBE','AMZN','MSFT','KO']
#list_stock=['META']

risk_free_rate = 2.24

list_short_sma = [50]
list_long_sma = [100,150,200]

list_short_rsi = [6,7]
list_long_rsi = [13,14]

rsi_range_period = 14

list_strategy = ['sma_crossover','rsi_range','rsi_crossover','support_resistance_breakout']

for strategy in list_strategy:

    df_hyp_test = pd.DataFrame()
    
    ######### Execute Strategies                            
    if strategy == 'sma_crossover':
        for short_sma in list_short_sma:
            for long_sma in list_long_sma: 
                df_analysis_heatmap = vs.gen_heatmap_df()    
                for ticker in list_stock :
                    try:
                        df_raw = uf.getdata(ticker, close = "Adj Close")   
                        df = sma_crossover.get_signal(df_raw, close='Adj Close', sma_value=[short_sma,long_sma], stop_loss_pct=0.03)
                        df_trades, df_heatmap = bt.df_backtesting(df, ticker, risk_free_rate)
                        title = 'Performance Metrics for sma_crossover with parameter ({},{})'.format(short_sma, long_sma)
                    except Exception as e:
                        print(f"Error occurred: {e}")
                        continue
                    df_analysis_heatmap = pd.concat([df_analysis_heatmap, df_heatmap])
                vs.gen_analysis_heatmap(df_analysis_heatmap, title)

    elif strategy == 'rsi_range':
        df_analysis_heatmap = vs.gen_heatmap_df()
        for ticker in list_stock :
            try:
                df_raw = uf.getdata(ticker, close = "Adj Close")   
                df = rsi_range.get_signal(df_raw, n_periods=rsi_range_period, close='Adj Close',overbought_threshold=70, oversold_threshold=30, stop_loss_pct=0.03)
                df_trades, df_heatmap = bt.df_backtesting(df, ticker, risk_free_rate)
                title = 'Performance Metrics for rsi_range with parameter {}'.format(rsi_range_period)
            except Exception as e:
                print(f"Error occurred: {e}")
                continue
            df_analysis_heatmap = pd.concat([df_analysis_heatmap, df_heatmap])
        vs.gen_analysis_heatmap(df_analysis_heatmap, title)

    elif strategy == 'rsi_crossover':            
        for short_rsi in list_short_rsi:
            for long_rsi in list_long_rsi:  
                df_analysis_heatmap = vs.gen_heatmap_df()
                for ticker in list_stock :
                    try:
                        df_raw = uf.getdata(ticker, close = "Adj Close")     
                        df = rsi_crossover.get_signal(df_raw, close="Adj Close", list_periods=[short_rsi,long_rsi], stop_loss_pct=0.03)
                        df_trades, df_heatmap =bt.df_backtesting(df, ticker, risk_free_rate)
                        title = 'Performance Metrics for rsi_crossover with parameter ({},{})'.format(short_rsi, long_rsi)
                    except Exception as e:
                        print(f"Error occurred: {e}")
                        continue
                    df_analysis_heatmap = pd.concat([df_analysis_heatmap, df_heatmap])
                vs.gen_analysis_heatmap(df_analysis_heatmap, title)

    elif strategy =='support_resistance_breakout':
        df_analysis_heatmap = vs.gen_heatmap_df()
        for ticker in list_stock :
            try:
                df_raw = uf.getdata(ticker, close = "Adj Close")  
                df = support_resistance_breakout.get_signal(df_raw, 'Adj Close', 60, 6, 10)
                df_trades, df_heatmap =bt.df_backtesting(df, ticker, risk_free_rate)
                title = 'Performance Metrics for support_resistance_breakout'
            except Exception as e:
                print(f"Error occurred: {e}")
                continue
            df_analysis_heatmap = pd.concat([df_analysis_heatmap, df_heatmap])
        vs.gen_analysis_heatmap(df_analysis_heatmap, title)
            # df_test = pd.DataFrame({ticker:df_trades['rate of return']})

        # df_hyp_test = pd.concat([df_hyp_test, df_test.reset_index(drop=True)], axis=1)
        
    
