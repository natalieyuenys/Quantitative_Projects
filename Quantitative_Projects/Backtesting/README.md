## Backtesting Repository

This repository contains a collection of scripts and tools for backtesting trading strategies.

### Objective:
- To identify which trading strategies work best for which stock
 
### Process of Backtest:
1. Choose trading strategy from `strategies.py`
   - **SMA Cross Over**: buy at previous day close if price> [Short SMA]>[Long SMA], sell at previous day close if price< [Short SMA]     
   - **Bollinger Bands**: buy at previous day close if price below lower bound, sell at previous day close if price above upper bound
   - **RSI**: sell at previous day close if rsi>overbought threshold, buy at previous day close if rsi<oversold threshold
   - **RSI Cross Over**: Buy at previous day close if [specified rsi]<rsi14, sell at previous day close if [specified rsi]>=rsi14
2. Choose backtest timeframe
   - Number of months
4. Allwo flesibility to choose combinations of parameters to check for one that performs best
5. Stop Loss 
   - If Price drops greater than a specified percentage, sell at previous day close even if sell condition is not met.  
6. Execute back-testing
7. Evaluate strategies, i.e. generate heatmap of below performance metrics across stocks
   - Strategy Return
   - Average rate of return
   - Best trade rate of return
   - Worst trade rate of return
   - Win Rate
   - Win-Loss Ratio
   - Sharpe Ratio

### Example of output
![alt text](./output/Performance%20Metrics%20for%20rsi_range%20with%20parameter%2014.png)

### Development:
- To add more strategies for testing
- To find out best combination of strategy and stock based on specific goal (by filtering on performance metrics)
- Use hypotheis testing to compare returns on each strategy for each stock