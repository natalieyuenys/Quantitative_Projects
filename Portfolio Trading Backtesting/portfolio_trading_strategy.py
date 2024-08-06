import pandas as pd
import tushare as ts
import backtrader as bt
import ta

from datetime import timedelta
import datetime
from datetime import datetime as dt

import matplotlib.pyplot as plt

import warnings
warnings.filterwarnings("ignore")

class MyStrategy(bt.Strategy):
    def __init__(self):
        self.selected_stocks = []
        self.observation_pool = []  # List to store stocks in the observation pool
        self.observation_rsi = {}
        self.observation_lowest_price = {}
        self.existing_holdings = []
        self.holdings={}

        self.equity_curve = []

        self.trade_log = pd.DataFrame(columns=['Date', 'Action','Price','Size','Symbol']) 
        for d in self.datas:
            data_name = d._name
            self.commission = TransactionCommission(data_name)
            self.broker.addcommissioninfo(self.commission)

    def get_market(self, symbol, trade_date):
        pro = ts.pro_api()
        market = pro.stock_basic(ts_code=symbol, list_status='L', trade_date=trade_date, fields='market').iloc[0,0]
        return market

    def get_stock_name(self, symbol, trade_date):
        pro = ts.pro_api()
        stock_name = pro.stock_basic(ts_code=symbol, list_status='L', trade_date=trade_date, fields='name').iloc[0,0]
        return stock_name

    def get_mktcap(self, symbol, trade_date):
        pro = ts.pro_api()
        mkp_cap = pro.daily_basic(ts_code=symbol, list_status='L', trade_date=trade_date, fields='circ_mv').iloc[0,0]
        return mkp_cap

    def get_suspend_list(self, trade_date):
        pro = ts.pro_api()    
        suspend_list = pro.suspend_d(suspend_type='S', trade_date=trade_date)['ts_code'].to_list()
        return suspend_list

    def screen_stocks(self, trade_date):
        self.selected_stocks=[]
        component_stocks = get_component_stock_list()

        for symbol in component_stocks:
            market = self.get_market(symbol, trade_date)
            if (symbol[-2:]=="SH" and market in ["主板","科创板"]) or (symbol[-2:]=="SZ" and market in ["主板","创业板"]):                
                suspend_list = self.get_suspend_list(trade_date)
                if symbol not in suspend_list:
                    stock_name = self.get_stock_name(symbol, trade_date)  
                    if 'ST' not in stock_name and '*ST' not in stock_name:
                        mkt_cap = self.get_mktcap(symbol, trade_date)
                        if mkt_cap/100000>=100:
                            self.selected_stocks.append(symbol)
    
    def check_stock(self):
        for d in self.datas:
            symbol = d._name
            if symbol in self.selected_stocks:
                if symbol not in self.observation_pool:
                    rsi = self.get_rsi(d)
                    prev_rsi = self.observation_rsi.get(symbol)
                    
                    print(rsi, prev_rsi)

                    if prev_rsi is not None and prev_rsi > 20 and rsi < 20:
                        self.observation_pool.append(symbol)

        print(f"Observation Pool: {self.observation_pool}")

        
    def check_observation_pool(self):
        for d in self.datas:
            symbol = d._name

            if symbol not in self.holdings:
                self.holdings[symbol] = {'quantity': 0, 'total_cost': 0}

            if symbol in self.observation_pool:
                rsi = self.get_rsi(d)
                lowest_price = self.get_lowest_price(symbol,d)

                prev_rsi = self.observation_rsi.get(symbol)
                prev_lowest_price = self.observation_lowest_price.get(symbol)
                print(rsi, prev_rsi, lowest_price, prev_lowest_price)

                if prev_rsi is not None and rsi > prev_rsi and rsi<=50 and lowest_price < prev_lowest_price:
                    if len(self.existing_holdings)<20:                    
                        trade = self.buy(data=d, size=self.calculate_position_size(), price=d.close[0])
                        self.existing_holdings.append(symbol)
                        self.holdings[symbol]['quantity'] += trade.size
                        self.holdings[symbol]['total_cost'] += trade.size * trade.price
                
                        self.trade_log = pd.concat([self.trade_log, pd.DataFrame({'Date': [d.datetime.datetime(0)],
                                                                                'Action':['Buy'],
                                                                            'Price': [trade.price],
                                                                            'Size': [trade.size],
                                                                            'Symbol':[symbol]})], ignore_index=True)
                elif prev_rsi is not None and rsi > 20:
                    self.observation_pool.remove(symbol)

    def check_existing_holdings(self):
        print(f"Existing Holdings: {self.existing_holdings}")
        for d in self.datas:
            symbol = d._name
                
            if symbol in self.existing_holdings:
                buy_price = self.holdings[symbol]['total_cost']/self.holdings[symbol]['quantity']
                stop_loss_threshold = buy_price * 0.02
                print(buy_price)

                if self.data.close[0] < buy_price - stop_loss_threshold:
                    trade = self.sell(data=d, size=self.holdings[symbol]['quantity'], price=d.open[1])
                    self.existing_holdings.remove(symbol)
                    self.holdings[symbol]['quantity'] += trade.size
                    self.holdings[symbol]['total_cost'] += trade.size * trade.price

                    self.trade_log = pd.concat([self.trade_log, pd.DataFrame({'Date': [d.datetime.datetime(0)],
                                                                  'Action':['Sell'],
                                                                  'Price': [d.open[1]],
                                                                  'Size':[trade.size],
                                                                  'Symbol':[symbol]})], ignore_index=True)
                rsi = self.get_rsi(d)
                prev_rsi = self.observation_rsi.get(symbol)

                if rsi > 20:
                    if prev_rsi is not None:
                        if rsi < prev_rsi and rsi < 50:
                            trade = self.sell(data=d, size=self.holdings[symbol]['quantity'], price=d.open[1])
                            self.existing_holdings.remove(symbol)
                            self.holdings[symbol]['quantity'] += trade.size
                            self.holdings[symbol]['total_cost'] += trade.size * trade.price

                            # Log the sell action
                            self.trade_log = pd.concat([self.trade_log, pd.DataFrame({'Date': [d.datetime.datetime(0)],
                                                                                'Action':['Sell'],
                                                                                'Price': [d.open[1]],
                                                                                'Size':[trade.size],
                                                                                'Symbol':[symbol]})], ignore_index=True)

                        if rsi >= 80:
                            trade = self.sell(data=d, size=self.holdings[symbol]['quantity'], price=d.open[1])
                            self.holdings[symbol]['quantity'] += trade.size
                            self.holdings[symbol]['total_cost'] += trade.size * trade.price

                            self.existing_holdings.remove(symbol)
                            # Log the sell action
                            self.trade_log = pd.concat([self.trade_log, pd.DataFrame({'Date': [d.datetime.datetime(0)],
                                                                                'Action':['Sell'],
                                                                                'Price': [d.open[1]],
                                                                                'Size':[trade.size],
                                                                                'Symbol':[symbol]})], ignore_index=True)

    def refresh_previous_values(self):
        for d in self.datas:
            symbol=d._name
            rsi = self.get_rsi(d)
            lowest_price = self.get_lowest_price(symbol,d)

            self.observation_rsi[symbol] = rsi
            self.observation_lowest_price[symbol] = lowest_price

    def get_rsi(self, d):
        close_values = []
        for i in range(30):
            close_values.append(d.close[-i])
        close_values = close_values[::-1]
        df = pd.DataFrame({'close':close_values})
        rsi = ta.momentum.RSIIndicator(df['close'], window=6).rsi()

        # Return the most recent RSI value
        return rsi.iloc[-1]
        
    def get_lowest_price(self, symbol, d):
        new_low = d.low[0]

        if self.observation_lowest_price.get(symbol) is not None:
            if new_low<self.observation_lowest_price.get(symbol):
                return new_low
            else:
                return self.observation_lowest_price.get(symbol)
        else:
            return new_low

    def calculate_position_size(self):
        total_value = self.broker.get_value()
        allocation = total_value * 0.05  # Allocation per stock
        position_size = allocation / self.data.close[0]
        rounded_position_size = round(position_size / 100) * 100
        return rounded_position_size

    def next(self):
        if self.datetime.date()<datetime.date(2021,1,1):
            pass

        else:
            if self.datetime.time() == datetime.time(9, 58):  # Screening process at the beginning of each day
                print(f"Backtesting for {self.datetime.date()}")
                trade_date = self.datetime.date().strftime("%Y%m%d")
                self.screen_stocks(trade_date)
                
            if len(self.existing_holdings) > 0:  
                self.check_existing_holdings()

            if len(self.observation_pool) > 0: 
                self.check_observation_pool()

            if len(self.selected_stocks) > 0:
                self.check_stock()

            self.equity_curve.append(self.broker.getvalue())
            self.refresh_previous_values()

def get_hourly_data(symbol, start_date, end_date, now):
    minute_data = ts.pro_bar(ts_code=symbol,start_date=start_date, end_date=end_date, freq='1min')   
    minute_data = minute_data.sort_values('trade_time')
    minute_data['trade_time'] = pd.to_datetime(minute_data['trade_time'])
    minute_data = minute_data[minute_data['trade_time']<=now]
    minute_data['rounded_hour'] = minute_data['trade_time'].apply(lambda x: x.replace(minute=0) if x.minute < 59 else x.replace(minute=0) + timedelta(hours=1))
    minute_data['rounded_hour'] = minute_data['rounded_hour']+ pd.DateOffset(minutes=58)

    # Resample the data to hourly frequency
    minute_data.set_index('trade_time', inplace=True)
    minute_data.index = pd.DatetimeIndex(minute_data.index)

    # Group the minute data by the hour ending at 58 minutes and perform aggregation
    hourly_data = minute_data.groupby('rounded_hour').agg({'open': 'first', 'high': 'max', 'low': 'min', 'close': 'last', 'vol': 'sum'})

    return hourly_data

def get_component_stock_list():
    pro = ts.pro_api()
    
    # Retrieve the component stocks
    SH_data = pro.index_weight(index_code='000001.SH', trade_date='20240131')
    SZ_data = pro.index_weight(index_code='399001.SZ', trade_date='20240131')

    data = pd.concat([SH_data, SZ_data], axis=0)

    # Filter component stocks based on non-zero weights
    component_stocks = data[data['weight'] > 0]['con_code'].tolist()

    listed_stocks = pro.stock_basic(list_status='L', fields='ts_code,list_date')
    listed_stocks = listed_stocks[listed_stocks['ts_code'].isin(component_stocks)]
    listed_stocks = listed_stocks[listed_stocks['list_date']<='20210101']['ts_code'].tolist()[690:700]

    return listed_stocks

class TransactionCommission(bt.CommInfoBase):
    params = (
        ('transaction_fee', 0.00025),  # Transaction fee rate (0.025% as an example)
        ('transfer_fee_per_thousand', 1.0),  # Transfer fee per thousand shares
        ('stamp_duty', 0.001),  # Stamp duty rate (0.1% as an example)
    )
    def __init__(self, data_name):
        super().__init__()
        self.data_name = data_name

    def _getcommission(self, size, price, pseudoexec):
        commission = abs(size) * price * self.p.transaction_fee
        if commission < 5.0:
            commission = 5.0

        if size<0:
            stamp_duty = abs(size) * price * self.p.stamp_duty
            if stamp_duty<1.0:
                stamp_duty=1.0
            commission += stamp_duty

        if self.data_name[-2:] == 'SH':
            share_count = abs(size) // 1000
            transfer_fee_share = share_count * self.p.transfer_fee_per_thousand
            commission += transfer_fee_share

        return commission
    
def plot_graph(df, equity_curve):

    datetimes = []

    for i in df.index:
        if datetime.datetime.strptime(str(i),"%Y-%m-%d %H:%M:%S")>datetime.datetime(2021,1,1,0,0,0):
            datetimes.append(i)

    # Plot the equity curve
    plt.plot(datetimes, equity_curve)
    plt.xlabel('Date')
    plt.ylabel('Equity Curve')
    plt.ticklabel_format(style='plain', axis='y', useOffset=False)
    plt.title('Equity Curve Plot')
    plt.grid(True)
    plt.savefig('Equity Curve.png')


def run_strategy():

    # Create an instance of cerebro
    cerebro = bt.Cerebro()

    lengths=[]
    for symbol in get_component_stock_list():
        print(f"Loading data for {symbol}...")
        # Use Tushare to get minute data for the current stock
        df_trunc_1 = get_hourly_data(symbol, '20210101', '20210201', (datetime.datetime(2021,2,1,0,0,0)))
        df_trunc_2 = get_hourly_data(symbol, '20210201', '20210301', (datetime.datetime(2021,3,1,0,0,0)))
        df_trunc_3 = get_hourly_data(symbol, '20210301', '20210401', (datetime.datetime(2021,4,1,0,0,0)))
        df_trunc_4 = get_hourly_data(symbol, '20210401', '20210501', (datetime.datetime(2021,5,1,0,0,0)))
        df_trunc_5 = get_hourly_data(symbol, '20210501', '20210601', (datetime.datetime(2021,6,1,0,0,0)))
        df_trunc_6 = get_hourly_data(symbol, '20210601', '20210701', (datetime.datetime(2021,7,1,0,0,0)))

        df = pd.concat([df_trunc_1,df_trunc_2,df_trunc_3,df_trunc_4,df_trunc_5,df_trunc_6]).sort_values('trade_time')
        df.index.name = 'trade_time' 
        data = bt.feeds.PandasData(dataname=df)
        lengths.append(len(df))
        if len(set(lengths)) > 1:
            raise AssertionError(f"{symbol} has a different data length.")
        else:
            cerebro.adddata(data, name=symbol)

    cerebro.addstrategy(MyStrategy)

    cerebro.broker.setcash(10000000) 

    # Run the strategy
    back = cerebro.run()

    # Plot the results
    equity_curve = back[0].equity_curve
    plot_graph(df, equity_curve)
    
    # Get the buy log DataFrame
    trade_log_df = back[0].trade_log

    # Print the buy log DataFrame
    print("Trade Log:")
    print(trade_log_df)
    trade_log_df.to_csv('output/trade_log.csv', index=False)

    # Print the final value
    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())

if __name__ == '__main__':
    run_strategy()