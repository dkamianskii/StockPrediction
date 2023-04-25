from typing import Optional
import pandas as pd
from ta.momentum import roc

from grpc_pbs.technical_indicators_pb2 import TRADE_ACTION_BUY, TRADE_ACTION_NONE, TRADE_ACTION_SELL, \
    TRADE_ACTION_STRONG_BUY, TRADE_ACTION_STRONG_SELL
from market_analytics_services.market_indicators.indicators_enums import TradeActionColumn, DataColumn, OneChannelColumn
from datetime import date


def RoC(data: pd.DataFrame,
        period: int,
        start_date: Optional[date] = None) -> pd.DataFrame:
    indicator_df = pd.DataFrame(data[DataColumn.DATE])
    indicator_df.columns = [TradeActionColumn.DATE]
    indicator_df[TradeActionColumn.ACTION] = TRADE_ACTION_NONE
    indicator_df[OneChannelColumn.VALUE] = roc(data[DataColumn.CLOSE], period)
    indicator_df.dropna(inplace=True)
    roc_trade_strategy(indicator_df, period)
    if start_date is None:
        return indicator_df
    else:
        return indicator_df.loc[start_date:]


def roc_trade_strategy(roc_df: pd.DataFrame, period: int):
    roc = roc_df[OneChannelColumn.VALUE]
    roc_mean = roc_df[OneChannelColumn.VALUE].rolling(15).mean()
    prev_mean = roc_mean.shift(1)
    prev2_mean = roc_mean.shift(2)
    action = TradeActionColumn.ACTION
    roc_df.loc[(roc_mean > period/2) & (roc_mean > prev_mean) & (prev_mean > prev2_mean), action] = TRADE_ACTION_BUY
    roc_df.loc[(roc_mean < -period/2) & (roc_mean < prev_mean) & (prev_mean < prev2_mean), action] = TRADE_ACTION_SELL
    roc_df.loc[roc >= 10, action] = TRADE_ACTION_STRONG_SELL
    roc_df.loc[roc <= -10, action] = TRADE_ACTION_STRONG_BUY
    prev_action = roc_df[action].shift(1)
    prev2_action = roc_df[action].shift(2)
    roc_df.loc[(roc_df[action] == TRADE_ACTION_BUY) &
           ((prev_action == TRADE_ACTION_STRONG_SELL) |
            (prev2_action == TRADE_ACTION_STRONG_SELL)), action] = TRADE_ACTION_NONE
    roc_df.loc[(roc_df[action] == TRADE_ACTION_SELL) &
           ((prev_action == TRADE_ACTION_STRONG_BUY) |
            (prev2_action == TRADE_ACTION_STRONG_BUY)), action] = TRADE_ACTION_NONE

