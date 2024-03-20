import numpy as np
import pandas as pd
import datetime
from dateutil.relativedelta import relativedelta

import ta
import talib
import yfinance as yf
import matplotlib.pyplot as plt

from sklearn.preprocessing import MinMaxScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import accuracy_score

from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.statespace.sarimax import SARIMAX
from sklearn.metrics import mean_squared_error


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
    
        ema_var_name = 'ema_' + str(i)
        df[ema_var_name] = ta.trend.ema_indicator(df['Close'],i)

        wma_var_name = 'wma_' + str(i)
        df[wma_var_name] = ta.trend.wma_indicator(df['Close'],i)

        # hma_var_name = 'hma_' + str(i)
        # df[hma_var_name] = ta.trend.hma_indicator(df['Close'],i)

        # tema_var_name = 'tema_' + str(i)
        # df[tema_var_name] = ta.trend.tema_indicator(df['Close'],i)

        # kama_var_name = 'kama_' + str(i)
        # df[kama_var_name] = ta.trend.kama_indicator(df['Close'],i)

    # Calculate the Bollinger Bands
    bb = ta.volatility.BollingerBands(close=df['Close'], window=20, window_dev=2)

    # Retrieve the upper, middle, and Lower bands
    df['upper_band'] = bb.bollinger_hband()
    df['middle_band'] = bb.bollinger_mavg()
    df['Lower_band'] = bb.bollinger_lband()

    df['bb_width'] = ta.volatility.bollinger_wband(df['Close'], window=20, window_dev=2)
    df['bb_percent'] = ta.volatility.bollinger_pband(df['Close'], window=20, window_dev=2)

    # Volume Indicators
    df['obv'] = ta.volume.on_balance_volume(df['Close'], df['Volume'])
    df['vwap'] = ta.volume.volume_weighted_average_price(df['High'], df['Low'], df['Close'], df['Volume'])
    # df['vp'] = ta.volume.volume_profile(df['Close'], df['Volume'])
    df['adl'] = ta.volume.acc_dist_index(df['High'], df['Low'], df['Close'], df['Volume'])

    # Trend Indicators
    df['adx'] = ta.trend.adx(df['High'], df['Low'], df['Close'])
    df['macd'] = ta.trend.macd(df['Close'])
    df['ichimoku_a'] = ta.trend.ichimoku_a(df['High'], df['Low'])
    df['ichimoku_b'] = ta.trend.ichimoku_b(df['High'], df['Low'])

    # Momentum Indicators
    df['rsi'] = ta.momentum.rsi(df['Close'])
    df['stoch'] = ta.momentum.stoch(df['High'], df['Low'], df['Close'])
    df['cci'] = ta.trend.cci(df['High'], df['Low'], df['Close'])
    df['roc'] = ta.momentum.roc(df['Close'])

    # Volatility Indicators
    df['atr'] = ta.volatility.average_true_range(df['High'], df['Low'], df['Close'])
    # df['natr'] = ta.volatility.normalized_average_true_range(df['High'], df['Low'], df['Close'])
    df['kc'] = ta.volatility.keltner_channel_hband_indicator(df['High'], df['Low'], df['Close'])

    # Oscillators
    df['uo'] = ta.momentum.ultimate_oscillator(df['High'], df['Low'], df['Close'])
    df['wr'] = ta.momentum.williams_r(df['High'], df['Low'], df['Close'])
    # df['ao'] = ta.momentum.ao(df['High'], df['Low'])

    # # Pattern Recognition
    df['doji'] = talib.CDLDOJI(df['Open'], df['High'], df['Low'], df['Close'])
    df['hammer'] = talib.CDLHAMMER(df['Open'], df['High'], df['Low'], df['Close'])
    df['engulfing'] = talib.CDLENGULFING(df['Open'], df['High'], df['Low'], df['Close'])
    df['harami'] = talib.CDLHARAMI(df['Open'], df['High'], df['Low'], df['Close'])

    df['lag_1_close'] = df[close].shift(1)
    df['lag_2_close'] = df[close].shift(2)
    df['lag_3_close'] = df[close].shift(3)
    
    return df

def data_preprocessing(df, close):

    df = df.dropna(subset=df.columns.tolist())
    df['next_day_close'] = df[close].shift(-1)
    df = df.dropna(subset=['next_day_close'])
    df = df.drop(columns='ticker')

    return df

def kmeans_elbow_method(df):
    wcss = []  # Within-Cluster Sum of Squares

    # Fit K-means clustering for different numbers of clusters
    for k in range(1, 12):
        kmeans = KMeans(n_clusters=k)
        kmeans.fit(df)
        wcss.append(kmeans.inertia_)  # Inertia is the WCSS

    # Plot the number of clusters vs. WCSS
    plt.plot(range(1, 12), wcss)
    plt.xlabel('Number of Clusters')
    plt.ylabel('WCSS')
    plt.title('Elbow Method')
    plt.show()

def detect_outliers_kmeans(data, n_clusters, percentile):
    # Perform K-means clustering
    kmeans = KMeans(n_clusters=n_clusters)
    kmeans.fit(data)
    
    # Calculate the distance of each sample to its Closest cluster centroid
    distances = kmeans.transform(data)
    min_distances = np.min(distances, axis=1)
    
    # Set a threshold to identify outliers as samples with large distances
    threshold = np.percentile(min_distances,percentile)
    outliers = data[min_distances > threshold]
    
    print("Number of outliers = {}".format(len(outliers)))

    return outliers

def df_min_max_scaler(df_x, df_y, scaler_x, scaler_y):

    scaler_x.fit(df_x)
    scaled_data_x = scaler_x.transform(df_x)
    df_scaled_x = pd.DataFrame(scaled_data_x, columns=df_x.columns)

    scaler_y.fit(df_y)
    scaled_data_y = scaler_y.transform(df_y)
    df_scaled_y = pd.DataFrame(scaled_data_y, columns=df_y.columns)

    return df_scaled_x, df_scaled_y

def apply_PCA(df_scaled_x):

    # Apply PCA

    pca = PCA(n_components=8)  # Specify the number of components you want to retain
    principal_components = pca.fit_transform(df_scaled_x)

    # Create a new DataFrame with the principal components
    df_pca_full_x = pd.DataFrame(data=principal_components)

    for i in df_pca_full_x.columns.to_list():
        var_rename = "PCA"+str(i)
        df_pca_full_x = df_pca_full_x.rename(columns={i:var_rename})
    
    return df_pca_full_x

def check_overfitting(df, relevant_indicators, scaler_y, window_size, step_size):

    for i in relevant_indicators[:-1]:

        mse_scores_test = []
        mse_scores_train = []
        
        df_temp = df[relevant_indicators].drop(columns=i)    
        # Perform rolling window cross-validation
        for start in range(0, len(df) - window_size + 1, step_size):
            
            end = start + window_size
            
            # Split the data into training and validation sets
            train_data = df_temp.iloc[start:end]
            test_data = df_temp.iloc[end:end+step_size]

            train_data_endog = train_data['next_day_close']
            train_data_exog = train_data.drop(columns='next_day_close')

            test_data_endog = test_data['next_day_close']
            test_data_exog = test_data.drop(columns='next_day_close')
            
            # Fit the ARIMAX model
            model = ARIMA(endog=train_data_endog, exog=train_data_exog, order=(0, 0, 0))
            model_fit = model.fit()

            # Make predictions
            test_predictions = model_fit.get_forecast(steps=len(test_data), exog=test_data_exog)
            train_predictions = model_fit.get_forecast(steps=len(train_data), exog=train_data_exog)

            val_predictions_mean = test_predictions.predicted_mean
            val_predictions_mean = val_predictions_mean.values.reshape(-1,1)
            test_pred = scaler_y.inverse_transform(val_predictions_mean)

            test_endo = test_data_endog.values.reshape(-1,1)
            test_endo = scaler_y.inverse_transform(test_endo)

            train_predictions_mean = train_predictions.predicted_mean
            train_pred = train_predictions_mean.values.reshape(-1,1)
            train_pred = scaler_y.inverse_transform(train_pred)

            train_endo = train_data_endog.values.reshape(-1,1)
            train_endo = scaler_y.inverse_transform(train_endo)

            #Calculate mean squared error (MSE) as the performance metric
            mse_test = mean_squared_error(test_endo, test_pred)
            mse_scores_test.append(round(mse_test,4))

            mse_train = mean_squared_error(train_endo, train_pred)
            mse_scores_train.append(round(mse_train,4))

        print("Remove {} = {}\n{}".format(i,mse_scores_test,mse_scores_train))

def find_best_order_arima_accuracy(train_data, test_data, df_y, train_size, scaler_y):
    train_data_endog = train_data['next_day_close']
    train_data_exog = train_data.drop(columns='next_day_close')

    test_data_endog = test_data['next_day_close']
    test_data_exog = test_data.drop(columns='next_day_close')
    
    best_accuracy=0
    for p in range(3):
            for d in range(2):
                    for q in range(3):
                        
                            model = ARIMA(endog=train_data_endog, exog=train_data_exog, order=(p, d, q))
                            model_fit = model.fit()

                            # Forecast on the test data
                            forecast = model_fit.get_forecast(steps=len(test_data), exog=test_data_exog)

                            # Get the predicted values
                            predicted_values = forecast.predicted_mean
                            val_predictions_mean = predicted_values.values.reshape(-1,1)
                            test_pred = scaler_y.inverse_transform(val_predictions_mean)
                            test_pred_series = pd.Series(test_pred.flatten())

                            # Calculate the price change from the predicted values
                            predicted_price_change = test_pred_series.diff()

                            # Create a binary target variable indicating if the price change is positive (1) or not (0)
                            predicted_price_up = (predicted_price_change > 0).astype(int)

                            # Calculate the actual price change from the test data
                            actual_price_change = df_y[train_size:].diff()

                            # Create a binary target variable for the actual price change
                            actual_price_up = (actual_price_change > 0).astype(int)

                            # Calculate the accuracy of the predictions
                            accuracy = accuracy_score(actual_price_up, predicted_price_up)

                            if best_accuracy<accuracy:
                                    best_accuracy = accuracy

                                    best_p, best_d, best_q = p,d,q
    #Print the accuracy
    print(f"Accuracy of best order ({best_p},{best_d},{best_q}) = {best_accuracy}")

    return best_accuracy

def find_best_order_sarimax_accuracy(train_data, test_data, df_y, train_size, scaler_y):

    # Specify the order and seasonal order of the SARIMA model
    seasonal_order = (1, 0, 0, 90)  # (P, D, Q, seasonal_periods)

    train_data_endog = train_data['next_day_close']
    train_data_exog = train_data.drop(columns='next_day_close')

    test_data_endog = test_data['next_day_close']
    test_data_exog = test_data.drop(columns='next_day_close')

    best_accuracy=0

    for p in range(3):
        for d in range(2):
            for q in range(3):
            
                # Create the SARIMA model
                model = SARIMAX(endog=train_data_endog, exog=train_data_exog, order=(p,d,q), seasonal_order=seasonal_order)

                # Fit the SARIMA model
                results = model.fit()

                # Forecast on the test data
                forecast = results.get_forecast(steps=len(test_data), exog=test_data_exog)

                # Get the predicted mean values
                predicted_values = forecast.predicted_mean
                val_predictions_mean = predicted_values.values.reshape(-1,1)
                test_pred = scaler_y.inverse_transform(val_predictions_mean)
                test_pred_series = pd.Series(test_pred.flatten())

                # Calculate the price change from the predicted values
                predicted_price_change = test_pred_series.diff()

                # Create a binary target variable indicating if the price change is positive (1) or not (0)
                predicted_price_up = (predicted_price_change > 0).astype(int)

                # Calculate the actual price change from the test data
                actual_price_change = df_y[train_size:].diff()

                # Create a binary target variable for the actual price change
                actual_price_up = (actual_price_change > 0).astype(int)

                # Calculate the accuracy of the predictions
                accuracy = accuracy_score(actual_price_up, predicted_price_up)

                if accuracy>best_accuracy:
                    best_accuracy = accuracy
                    best_p, best_d, best_q = p,d,q

    # Print the accuracy
    print(f"Accuracy: {best_accuracy} with order ({best_p},{best_d},{best_q})")

    return best_accuracy