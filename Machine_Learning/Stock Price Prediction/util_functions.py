import numpy as np
import pandas as pd
import datetime
from dateutil.relativedelta import relativedelta

import yfinance as yf
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

def SMA(df, n, close):
    return pd.Series(df[close]).rolling(n).mean()

def getdata(sym, sma_value, close):
    today = datetime.datetime.now()
    df=yf.download(sym, start=datetime.datetime(today.year-1, 1, 1),
                   end=datetime.datetime(today.year, today.month, today.day))
    pd.set_option('display.max_columns', None)

    df = df[['Open','High','Low',close,'Volume']]
    df = df.reset_index().rename(columns={'index':'Date'})
    df['ticker'] = sym

    for i in sma_value:
        variable_name = 'sma_' + str(i)
        df[variable_name] = SMA(df, i, close)

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

def detect_outliers_kmeans(data, n_clusters):
    # Perform K-means clustering
    kmeans = KMeans(n_clusters=n_clusters)
    kmeans.fit(data)
    
    # Calculate the distance of each sample to its closest cluster centroid
    distances = kmeans.transform(data)
    min_distances = np.min(distances, axis=1)
    
    # Set a threshold to identify outliers as samples with large distances
    threshold = np.percentile(min_distances,85)
    outliers = data[min_distances > threshold]
    
    return outliers