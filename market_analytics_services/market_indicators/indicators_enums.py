from enum import Enum


class DataColumn(Enum):
    DATE = 0
    OPEN = 1
    CLOSE = 2
    HIGH = 3
    LOW = 4


class TradeActionColumn(Enum):
    DATE = 0
    ACTION = 1


class OneChannelColumn(Enum):
    VALUE = 0


class MACDColumn(Enum):
    MACD = 0
    SIGNAL = 1
    DIFF = 2


class BollingerBandsColumn(Enum):
    LOWER_BAND = 0
    MA = 1
    UPPER_BAND = 2


class RVIColumn(Enum):
    RVI = 0
    SIGNAL = 1


class AlligatorColumn(Enum):
    LIPS = 0
    TEETH = 1
    JAW = 2


if __name__ == "__main__":
    for m in DataColumn:
        print(m)
