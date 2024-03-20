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
- Check for overfitting
- PCA (Principal component Analysis) to reduce dimentionality

**4. Fit Model** 
- Find best order - with highest accuracy rate

**5. Result**
- Highest Accuracy rate of predicting next day's stock price direction of `GOOG` with ARIMA order (0,1,2) = 66.7%
