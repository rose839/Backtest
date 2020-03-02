import pandas as pd
import numpy as np
from numbers import Number
frome utils import assert_msg, read_file

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

