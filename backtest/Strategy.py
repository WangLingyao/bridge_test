import backtrader as bt
import pandas as pd
import tushare as ts
from datetime import datetime
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

def data_get(stock_code='000001.SZ',startday='20230101',endday='20231231'):
    pro = ts.pro_api('9a30091fee2aafa8e326b93a79c3dc51ca7fb7bc7f13fe6765582087')
    df = pro.query('daily', ts_code=stock_code, start_date=startday, end_date=endday)
    df.index=pd.to_datetime(df['trade_date'])
    df['openinterest']=0
    df.rename(columns={'vol':'volume'},inplace=True)
    df=df[['open','high','low','close','volume','openinterest']]
    df = df.sort_index()
    return df

def run_backtest(stock_code,start_date,end_date,principal=1000000,buy_percent=0.2):
    start_date = datetime.strptime(start_date, "%Y%m%d")
    end_date = datetime.strptime(end_date, "%Y%m%d")
    stock_df = data_get(stock_code,start_date.strftime('%Y%m%d'), end_date.strftime('%Y%m%d'))
    startcash=principal

    # 当12日的价格均线穿越26日的价格均线时买入。当价格跌破26均线时卖出。
    class MyStrategy(bt.Strategy):
        params = (
            ('longperiod', 26),
            ('shortperiod', 12)
        )

        def __init__(self, principal=1000000, buy_percent=0.2):
            self.principal = principal
            self.buy_percent = buy_percent
            self.order = None
            self.mean2 = bt.indicators.SimpleMovingAverage(self.data.close, period=self.params.longperiod)
            self.mean1 = bt.indicators.SimpleMovingAverage(self.data.close, period=self.params.shortperiod)
            self.logs = []

        def log(self, txt, dt=None):
            dt = dt or self.data.datetime.date(0)
            log_message = f'date:{dt.isoformat()}, {txt}'
            self.logs.append(log_message)

        def notify_order(self, order):
            total_value = self.broker.getvalue()

            if order.status in [order.Submitted, order.Accepted]:
                return

            if order.status in [order.Completed]:
                if order.isbuy():
                    self.log('买入订单已执行-价格：%.2f,当前总资产：%.2f'%(order.executed.price,total_value))
                elif order.issell():
                    self.log('卖出订单已执行-价格：%.2f,当前总资产：%.2f'%(order.executed.price,total_value))

            self.order = None

        def next(self):
            total_value = self.broker.getvalue()

            if not self.position:
                if self.mean1[0] > self.mean2[0]:
                    # 计算以当前本金的20%买入的股数
                    buy_size = (total_value * self.buy_percent) / self.data.open[0]
                    self.order = self.buy(size=buy_size)

            else:
                if self.mean1[0] < self.mean2[0]:
                    # 获取当前仓位，卖出所有持仓
                    current_position = self.position.size
                    self.order = self.sell(size=current_position)

    cerebro = bt.Cerebro()
    datafeed = bt.feeds.PandasData(dataname=stock_df, fromdate=start_date, todate=end_date)
    cerebro.adddata(datafeed)
    cerebro.addstrategy(MyStrategy,principal=startcash, buy_percent=buy_percent)
    cerebro.broker = bt.brokers.BackBroker(slip_perc=0.0001)
    cerebro.broker.setcash(startcash)

    # 添加回测指标
    cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name='tradeanalyzer')
    cerebro.addanalyzer(bt.analyzers.AnnualReturn, _name='annualReturn')  # 年度回报
    cerebro.addanalyzer(bt.analyzers.Returns, _name='_Returns', tann=252)  # 年化收益
    cerebro.addanalyzer(bt.analyzers.DrawDown, _name='drawdown')  # 回撤
    cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name='sharpe')  # 夏普率
    cerebro.addanalyzer(bt.analyzers.Returns, _name='returns')  # 收益
    cerebro.addanalyzer(bt.analyzers.TimeReturn, _name='_TimeReturn')

    results = cerebro.run()
    strategy = results[0]
    log = strategy.logs


    return {
        '初始总资产:':startcash,
        '最终总资产:': cerebro.broker.getvalue(),
        '累计收益率%:': results[0].analyzers.returns.get_analysis()['rtot'],
        '年化收益率%:': results[0].analyzers._Returns.get_analysis()['rnorm100'],
        '最大回撤比例%:': results[0].analyzers.drawdown.get_analysis().max.drawdown,
        '交易详情': log
    }














