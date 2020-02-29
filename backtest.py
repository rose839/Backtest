import pandas as pd
import numpy as np

class Backtest(object):
    """
    Backtest class, used for read history market data, execute strategy,
    simulate transaction and compute profit
    """

    def __init__(self,
                 data: pd.DataFrame,
                 strategy_type: type(Strategy),
                 broker_type: type(Broker),
                 cash: float = 10000,
                 commission: float = .0):
        pass