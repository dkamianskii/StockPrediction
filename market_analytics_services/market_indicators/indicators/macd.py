from typing import Optional

import numpy as np
import pandas as pd
from ta.trend import MACD as macd

from grpc_pbs.technical_indicators_pb2 import TRADE_ACTION_BUY, TRADE_ACTION_NONE, TRADE_ACTION_SELL, \
    TRADE_ACTION_STRONG_BUY, TRADE_ACTION_STRONG_SELL
from market_analytics_services.market_indicators.indicators_enums import TradeActionColumn, DataColumn, MACDColumn


def MACD(data: pd.DataFrame,
         fast_period: Optional[int] = None,
         slow_period: Optional[int] = None,
         signal_period: Optional[int] = None,
         start_date: Optional[pd.Timestamp] = None) -> pd.DataFrame:
    fast_period = 12 if fast_period is None else fast_period
    slow_period = 26 if slow_period is None else slow_period
    signal_period = 9 if signal_period is None else signal_period
    indicator_df = pd.DataFrame(data[DataColumn.DATE])
    indicator_df.columns = [TradeActionColumn.DATE]
    indicator_df[TradeActionColumn.ACTION] = TRADE_ACTION_NONE
    calculated = macd(data[DataColumn.CLOSE], fast_period, slow_period, signal_period)
    indicator_df[MACDColumn.MACD] = calculated.macd()
    indicator_df[MACDColumn.SIGNAL] = calculated.macd_signal()
    indicator_df[MACDColumn.DIFF] = calculated.macd_diff()
    indicator_df.dropna(inplace=True)
    macd_trade_strategy(indicator_df)
    if start_date is None:
        return indicator_df
    else:
        return indicator_df.loc[start_date:]


def macd_trade_strategy(macd_df):
    macd = macd_df[MACDColumn.MACD]
    diff = macd_df[MACDColumn.DIFF]
    diff_prev = diff.shift(1)
    sus_map = (diff == 0) | (np.sign(diff_prev) != np.sign(diff))
    action = TradeActionColumn.ACTION
    macd_df.loc[sus_map & (np.sign(diff_prev) > 0), action] = TRADE_ACTION_SELL
    macd_df.loc[sus_map & (np.sign(diff_prev) > 0) & (macd > 0), action] = TRADE_ACTION_STRONG_SELL
    macd_df.loc[sus_map & (np.sign(diff_prev) < 0), action] = TRADE_ACTION_BUY
    macd_df.loc[sus_map & (np.sign(diff_prev) < 0) & (macd < 0), action] = TRADE_ACTION_STRONG_BUY
