from typing import Optional

import numpy as np
import pandas as pd
from ta.momentum import rsi

from grpc_pbs.technical_indicators_pb2 import TRADE_ACTION_BUY, TRADE_ACTION_NONE, TRADE_ACTION_SELL, \
    TRADE_ACTION_STRONG_BUY, TRADE_ACTION_STRONG_SELL
from market_analytics_services.market_indicators.indicators_enums import TradeActionColumn, DataColumn, OneChannelColumn


def RSI(data: pd.DataFrame,
        period: int,
        start_date: Optional[pd.Timestamp] = None) -> pd.DataFrame:
    indicator_df = pd.DataFrame(data[DataColumn.DATE])
    indicator_df.columns = [TradeActionColumn.DATE]
    indicator_df[TradeActionColumn.ACTION] = TRADE_ACTION_NONE
    indicator_df[OneChannelColumn.VALUE] = rsi(data[DataColumn.CLOSE], period)
    indicator_df.dropna(inplace=True)
    rsi_trade_strategy(indicator_df)
    if start_date is None:
        return indicator_df
    else:
        return indicator_df.loc[start_date:]


def rsi_trade_strategy(rsi_df):
    rsi = rsi_df[OneChannelColumn.VALUE]
    rsi_prev = rsi.shift(1)
    action = TradeActionColumn.ACTION
    rsi_df.loc[rsi >= 80, action] = TRADE_ACTION_STRONG_SELL
    rsi_df.loc[rsi <= 20, action] = TRADE_ACTION_STRONG_BUY
    rsi_df.loc[(rsi < 70) & (rsi >= 67.5) & (rsi_prev >= 70), action] = TRADE_ACTION_SELL
    rsi_df.loc[(rsi > 30) & (rsi <= 32.5) & (rsi_prev <= 30), action] = TRADE_ACTION_BUY
    rsi_df.loc[(rsi >= 70) &
               (rsi_prev >= 70) &
               ((np.abs(rsi - rsi_prev) >= 5) | (rsi < 70.5)), action] = TRADE_ACTION_SELL
    rsi_df.loc[(rsi <= 30) &
               (rsi_prev <= 30) &
               ((np.abs(rsi - rsi_prev) >= 5) | (rsi > 29.5)), action] = TRADE_ACTION_BUY
