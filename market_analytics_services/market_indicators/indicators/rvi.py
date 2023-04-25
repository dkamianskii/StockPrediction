from typing import Optional

import numpy as np
import pandas as pd

from grpc_pbs.technical_indicators_pb2 import TRADE_ACTION_BUY, TRADE_ACTION_NONE, TRADE_ACTION_SELL, \
    TRADE_ACTION_STRONG_BUY, TRADE_ACTION_STRONG_SELL
from market_analytics_services.market_indicators.indicators_enums import TradeActionColumn, DataColumn, RVIColumn
from datetime import date


def RVI(data: pd.DataFrame,
        smoothing_period: Optional[int] = None,
        start_date: Optional[date] = None) -> pd.DataFrame:
    smoothing_period = 10 if smoothing_period is None else smoothing_period
    indicator_df = pd.DataFrame(data[DataColumn.DATE])
    indicator_df.columns = [TradeActionColumn.DATE]
    indicator_df[TradeActionColumn.ACTION] = TRADE_ACTION_NONE
    weights = [1/6, 1/3, 1/3, 1/6]
    numerator = (data[DataColumn.CLOSE] - data[DataColumn.OPEN]).rolling(4).apply(lambda x: (x * weights).sum())
    denominator = (data[DataColumn.HIGH] - data[DataColumn.LOW]).rolling(4).apply(lambda x: (x * weights).sum())
    rvi = numerator.rolling(smoothing_period).mean() / denominator.rolling(smoothing_period).mean()
    signal = rvi.rolling(4).apply(lambda x: (x * weights).sum())
    indicator_df[RVIColumn.RVI] = rvi
    indicator_df[RVIColumn.SIGNAL] = signal
    indicator_df.dropna(inplace=True)
    rvi_trade_strategy(indicator_df)
    if start_date is None:
        return indicator_df
    else:
        return indicator_df.loc[start_date:]


def rvi_trade_strategy(rvi_df):
    diff = rvi_df[RVIColumn.RVI] - rvi_df[RVIColumn.SIGNAL]
    diff_prev = diff.shift(1)
    sus_buy = np.sign(diff_prev) < np.sign(diff)
    sus_sell = np.sign(diff_prev) > np.sign(diff)
    action = TradeActionColumn.ACTION
    rvi_df.loc[sus_buy & (rvi_df[RVIColumn.RVI] < -0.2), action] = TRADE_ACTION_BUY
    rvi_df.loc[sus_buy & (rvi_df[RVIColumn.RVI] < -0.35), action] = TRADE_ACTION_STRONG_BUY
    rvi_df.loc[sus_sell & (rvi_df[RVIColumn.RVI] > 0.2), action] = TRADE_ACTION_SELL
    rvi_df.loc[sus_sell & (rvi_df[RVIColumn.RVI] > 0.35), action] = TRADE_ACTION_STRONG_SELL

