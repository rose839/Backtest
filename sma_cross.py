import pandas as pd

def SMA(values, n):
    """
    Caculate SMA
    :param values:
    :param n:
    :return:
    """
    return pd.Series(values).rolling(n).mean()

def crossover(series1, series2) -> bool:
    """
    Check two series whether cross at the end.
    """
    return series1[-2] < series2[-2] and series1[-1] > series2[-1]

class SmaClass(Strategy):
    # SMA fast line
    fast = 30

    # SMA slow line
    slow = 90

    def init(self):
        # caculate fast and slow line at every time point
        self.sma1 = self.calculate_indicators(SMA, self.data.Close, self.fast)
        self.sma2 = self.calculate_indicators(SMA, self.data.Close, self.slow)

    def next(self, tick):
        # fast catch up and beyond slow, buy in
        if crossover(self.sma1[:tick], self.sma2[:tick]):
            self.buy()
        # slow get cross fast, buy in
        elif crossover(self.sma2[:tick], self.sma1[:tick]):
            self.sell()
        else:
            pass




