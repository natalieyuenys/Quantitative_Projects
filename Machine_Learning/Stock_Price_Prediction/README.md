# Stock Price Prediction

This repo is for predicting the direction of next day's stock price.

Steps: 

**1. Load data** 

**2. Data Pre-processing** 
- Remove NA
- Remove outliers
- MinMaxScaler

**3. Feature Engineering: Identify relavant variables** 
- Calculate Correlations
- Check for overfitting with cross-validation
- PCA (Principal component Analysis) to reduce dimentionality

**4. Fit Model** 
- Find best order - with highest accuracy rate

**5. Result**
- Highest Accuracy rate of predicting next day's stock price direction for below stocks
    - `META` with SMA20 and SMA200 = 76.4%
    - `TELA` with SMA50 and SMA100 = 75.8%
    - `APPL` with SMA10 and SMA200 = 70.6%
    - `GOOG` with SMA20 and SMA200 = 70.6%
    - `NVDA` with SMA10 and SMA100 = 66.7%
    - `AMZN` with SMA20 and SMA200 = 64.7%
    - `ADBE` with SMA10 and SMA150 = 60.0%
    - `KO` with SMA10 and SMA200 = 58.8%
    - `MSFT`with SMA10 and SMA200 = 58.8%
