import warnings
warnings.filterwarnings("ignore")

import pandas as pd
import datetime

import statsmodels.formula.api as sm
from sklearn.preprocessing import MinMaxScaler

import util_functions as uf

############### Parameter Control ##########
today = datetime.datetime.now()
end_date = datetime.datetime(today.year, today.month, today.day)
start_date = datetime.datetime(today.year-1, 1, 1)

short_sma_list = [10,20,50]
long_sma_list = [100,150,200]

################### Run Code ################
best_accuracy = 0

for short_sma in short_sma_list:
    for long_sma in long_sma_list:

        print(f"Testing for SMA{short_sma} and SMA{long_sma}...")
        df = uf.getdata('GOOG',[short_sma, long_sma],'Close', start_date, end_date)

        df = uf.data_preprocessing(df, 'Close')

        df_outliers = uf.detect_outliers_kmeans(df.drop(columns='Date'), 4, 80)

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

        accuracy = uf.find_best_order_arima_accuracy(train_data, test_data, df_y, train_size, scaler_y)

        if accuracy>best_accuracy:
            best_accuracy=accuracy
            best_short_sma, best_long_sma = short_sma, long_sma

print(f"Accuracy with SMA{best_short_sma} and SMA{best_long_sma} = {best_accuracy}")

