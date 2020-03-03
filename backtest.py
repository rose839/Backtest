import pandas as pd
import numpy as np
from numbers import Number
from exchangeAPI import ExchangeAPI
from strategy import Strategy
from sma_cross import SmaClass
from utils import assert_msg, read_file

class Backtest(object):
    """
    Backtest class, used for read history market data, execute strategy,
    simulate transaction and compute profit
    """

    def __init__(self,
                 data: pd.DataFrame,
                 strategy_type: type(Strategy),
                 broker_type: type(ExchangeAPI),
                 cash: float = 10000,
                 commission: float = .0):
        """
        Init backtest object, include check param type, fill null data.

        Params:
        :param data:            pd.DataFrame      history data in DataFrame
        :param strategy_type:   type(Strategy)    strategy class
        :param broker_type:     type(ExchangeAPI) ExchangeAPI class, execute
                                                  buy and sell, maintain account
                                                  state
        :param cash:            float             initial cash
        :param commission:      float             commission for every trade
        """

        assert_msg(issubclass(strategy_type, Strategy),    "strategy_type is not a Strategy type")
        assert_msg(issubclass(broker_type,   ExchangeAPI), "broker_type is not a ExchangeAPI type")
        assert_msg(isinstance(commission,    Number),      "commission is not a Number type")

        data = data.copy(False)

        if 'Volume' not in data:
            data['Volume'] = np.nan

        # verify OHLC data format
        assert_msg(len(data.columns & {'Open', 'High', 'Low', 'Close', 'Volume'}) == 5,
                   ("Data format not correct, need those columns folowing at least: "
                    "'Open', 'High', 'Low', 'Close'"))

        # sort as date
        if not data.index.is_monotonic_increasing:
            data = data.sort_index()

        # init object
        self._data = data
        self._broker = broker_type(data, cash, commission)
        self._strategy = strategy_type(self._broker, self._data)
        self._results = None

    def run(self) -> pd.Series:
        """
        Run the backtest. Returns `pd.Series` with results and statistics.
        """
        strategy = self._strategy
        broker   = self._broker

        # strategy init
        strategy.init()

        # set backtest start and end position in data
        start = 100
        end = len(self._data)

        # backtest main loop, update market state, and execute strategy
        for i in range(start, end):
            # update market state first, then execute strategy
            broker.next(i)
            strategy.next(i)

        # after execute strategy, compute result and return
        self._results = self._compute_result(broker)
        return self._results

    def _compute_result(self, broker):
        s = pd.Series()
        s['initial value'] = broker.initial_cash
        s['ending value']  = broker.market_value
        s['profit']        = broker.market_value - broker.initial_cash
        return s

def main():
    data = read_file('test.csv')
    ret = Backtest(data, SmaClass, ExchangeAPI, 10000.0, 0.003).run()
    print(ret)

if __name__ == '__main__':
    main()