### Portfolio Trading Backtesting


##### Stock Selection
Among all the stocks in the Shanghai Stock Exchange (including the Science and Technology Innovation Board) and the Shenzhen Stock Exchange (including the ChiNext Board):

- Non-ST (Special Treatment) stocks, non-*ST (Special Treatment) stocks
- Stocks with market capitalization greater than 100 billion
- Stocks that are not suspended from trading on the current day
- Scan the stock pool before the market opens every day to determine the selection pool, and do not change the selection pool during the trading day due to changes in intraday market capitalization (less than 100 billion)


##### Observation Pool
1. When observing the RSI value of the stocks in the observation pool, if the RSI value enters from >20 (including 20) to <20, the tracking is triggered. Note: It must be a drop from greater than 20 to less than 20 to trigger it, the first time the value is captured, if the previous value is already <20, it does not count.
2. The time point of data collection is unified at the last minute of each hour, that is, from XX:58 to start collecting and observing.
3. After the start of the next hour, refresh the RSI value and the lowest stock price of the previous hour (correct the value taken at 58 minutes), and use the updated value for subsequent comparisons.
4. After the observation is triggered, continue to observe the hourly RSI value until the buy trigger condition is met or the RSI value returns above 20 and exits the observation.
5. Entry Criteria: The stock price hits a new low (including the lower shadow, not the hourly closing price) + RSI does not hit a new low (above 20 is counted, above 50 is not counted) - "indicator divergence". Example: After the observation is triggered, a total of 5 hours are observed, and the lowest price in these 5 hours is 20 yuan, the lowest hourly RSI is 18. In the 6th hour, the lowest price is 19.5 yuan, and the hourly RSI is 19 or 21, then the buy trigger condition is met. But if the RSI is 17, continue to observe. Note: Follow the second rule, look at the time at the end of the day, not during the day.
6. If the "indicator divergence" occurs consecutively, the buy (equal amount) will be triggered consecutively.
7. Referring to the 4th point, if the RSI appears >20, and the "indicator divergence" does not occur, exit the observation and remove it from the observation pool.


##### Exit Criteria
1. After buying, at any time, if the hourly closing price is lower than the buy price (if multiple purchases, look at the average cost) by 2% or more, close the position with a stop loss (look at the price before the 57-minute closing auction each day).
2. Wait for the hourly RSI value to be greater than 20, and the prerequisite for all other profit-taking sell actions, except for the stop loss, is that the hourly RSI value is greater than 20:   
    2.1. When the hourly RSI value is lower than the previous hour's value + the current hour's RSI value is <50, close the position.
    2.2. When the hourly RSI value is lower than the previous hour's value + (50 (including 50) < the current hour's RSI value < 80), continue to observe.
    2.3. When the hourly RSI value is >80 (including 80) at any time point, close the position.
3. If the buy is placed on the same trading day, and the sell condition is triggered, sell during the next day's opening auction on T+1.

