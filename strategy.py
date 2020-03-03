import abc
import numpy as np
from typing import Callable
from utils import assert_msg

class Strategy(metaclass=abc.ABCMeta):
    """
    Abstract class, used to define trade strategy.
    User defined strategy need inherit this abstract class,
    and implement two abstract method:
        Strategy.init
        Strategy.next
    """
    def __init__(self, broker, data):
        self._indicators = []
        self._broker = broker
        self._data = data
        self._tick = 0

    def calculate_indicators(self, func: Callable, *args) -> np.ndarray:
        """
        Indicators is an array, its length is same as history data, used to
        check buy or sell at this point.
        """
        value = func(*args)
        value = np.asarray(value)
        assert_msg(value.shape[-1] == len(self._data.Close), "indicators's length must be same as data")

        self._indicators.append(value)
        return value

    @property
    def tick(self):
        return self._tick

    @abc.abstractmethod
    def init(self):
        pass

    @abc.abstractmethod
    def next(self):
        pass

    def buy(self):
        self._broker.buy()

    def sell(self):
        self._broker.sell()

    @property
    def data(self):
        return self._data


