from utils import assert_msg

class ExchangeAPI(object):
    def __init__(self, data, cash, commission):
        """
        :param data:       pd.DataFrame  market data
        :param cash:       float         initial cash
        :param commission: float         commission for every trade
        :return:
        """

        assert_msg(0 < cash, 'Initial cash must be greater than 0, input cash: {}'.format(cash))
        assert_msg(0 <= commission <= 0.05, "Resonable commission won't be less than 0.05, input: {}".format(commission))

        self._initial_cash = cash
        self._data = data
        self._commission = commission
        self._position = 0 # current account position
        self._cash = cash  # current cash in account
        self._cursor = 0   # corrent position in data

    @property
    def cash(self):
        return self._cash

    @property
    def position(self):
        return self._position

    @property
    def initial_cash(self):
        return self._initial_cash

    @property
    def market_value(self):
        return self._cash + self._position * self.current_price

    @property
    def current_price(self):
        return self._data.Close[self._cursor]

    def buy(self):
        """
        Buying in as market value using spare cash in account
        :return:
        """
        self._position = float(self._cash * (1 - self._commission) / self.current_price)
        self._cash = 0.0

    def sell(self):
        """
        Selling out all position
        :return:
        """
        self._cash += float(self._position * self.current_price * (1 - self._commission))
        self._position = 0.0

    def next(self, tick):
        self._cursor = tick