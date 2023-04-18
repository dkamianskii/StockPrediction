from typing import Optional

import numpy as np
import pandas as pd

from grpc_pbs.technical_indicators_pb2 import TRADE_ACTION_BUY, TRADE_ACTION_NONE, TRADE_ACTION_SELL, \
    TRADE_ACTION_STRONG_BUY, TRADE_ACTION_STRONG_SELL
from market_analytics_services.market_indicators.indicators_enums import TradeActionColumn, DataColumn, RVIColumn


def RVI(data: pd.DataFrame,
        smoothing_period: Optional[int] = None,
        signal_period: Optional[int] = None,
        start_date: Optional[pd.Timestamp] = None) -> pd.DataFrame:
    smoothing_period = 10 if smoothing_period is None else smoothing_period
    signal_period = 4 if signal_period is None else signal_period
    indicator_df = pd.DataFrame(data[DataColumn.DATE])
    indicator_df.columns = [TradeActionColumn.DATE]
    indicator_df[TradeActionColumn.ACTION] = TRADE_ACTION_NONE
    rvi = ((data[DataColumn.CLOSE] - data[DataColumn.OPEN]) / (data[DataColumn.HIGH] - data[DataColumn.LOW])).rolling(smoothing_period).mean()
    indicator_df[RVIColumn.RVI] = rvi
    indicator_df[RVIColumn.SIGNAL] = rvi.rolling(signal_period).mean()
    indicator_df.dropna(inplace=True)
    rvi_trade_strategy(indicator_df)
    if start_date is None:
        return indicator_df
    else:
        return indicator_df.loc[start_date:]


def rvi_trade_strategy(rvi_df):
    diff = rvi_df[RVIColumn.RVI] - rvi_df[RVIColumn.SIGNAL]
    diff_prev = diff.shift(1)
    sus_map = (diff == 0) | (np.sign(diff_prev) != np.sign(diff))
    action = TradeActionColumn.ACTION
    rvi_df.loc[sus_map & (np.sign(diff) >= 0), action] = TRADE_ACTION_SELL
    rvi_df.loc[sus_map & (np.sign(diff) <= 0), action] = TRADE_ACTION_BUY

