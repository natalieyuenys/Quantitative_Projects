import warnings
warnings.filterwarnings("ignore")

import pandas as pd
import datetime

import statsmodels.formula.api as sm
from sklearn.preprocessing import MinMaxScaler

import util_functions as uf

import logging


############### Parameter Control ##########
stock_list = ['AAPL','TSLA','NVDA','GOOG','META','ADBE','AMZN','MSFT','KO']

today = datetime.datetime.now()
end_date = datetime.datetime(today.year, today.month, today.day-1)
start_date = datetime.datetime(today.year-1, 1, 1)

short_sma_list = [10,20,50]
long_sma_list = [100,150,200]

################### Run Code ################
for stock in stock_list:    
    
    # Create a new logger instance for each stock
    logger = logging.getLogger(stock)
    logger.setLevel(logging.INFO)

    # Configure the logging settings for each stock
    logfile = f'Quantitative_Projects/Machine_Learning/Stock_Price_Prediction/output/{stock}_prediction_output.log' 
    file_handler = logging.FileHandler(logfile)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Main Code
    best_accuracy = 0

    for short_sma in short_sma_list:
        for long_sma in long_sma_list:

            # Add log messages to your code
            logger.info(f"Testing for SMA{short_sma} and SMA{long_sma}...")

            df = uf.getdata(stock,[short_sma, long_sma],'Close', start_date, end_date)

            df = uf.data_preprocessing(df, 'Close')

            df_outliers = uf.detect_outliers_kmeans(df.drop(columns='Date'), 4, 80, logger)

            df = df[~df.index.isin(df_outliers.index.tolist())]

            df_x = df.drop(columns=['Date','next_day_close'])
            df_y = df[['next_day_close']]

            scaler_x = MinMaxScaler()
            scaler_y = MinMaxScaler()

            df_scaled_x, df_scaled_y = uf.df_min_max_scaler(df_x, df_y, scaler_x, scaler_y)

            df_pca_full_x = uf.apply_PCA(df_scaled_x)

            warnings.filterwarnings("ignore")
            df = pd.concat([df_pca_full_x, df_scaled_y], axis=1)

            df = df.fillna(0)

            train_size = int(len(df) * 0.8)  # 80% for training
            train_data = df[:train_size]
            test_data = df[train_size:]

            accuracy = uf.find_best_order_arima_accuracy(train_data, test_data, df_y, train_size, scaler_y, logger)

            if accuracy>best_accuracy:
                best_accuracy=accuracy
                best_short_sma, best_long_sma = short_sma, long_sma

    logger.info(f"Accuracy with SMA{best_short_sma} and SMA{best_long_sma} = {best_accuracy}")
