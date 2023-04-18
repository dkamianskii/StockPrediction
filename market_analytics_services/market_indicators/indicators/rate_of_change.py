from typing import Optional
import pandas as pd
from ta.momentum import roc

from grpc_pbs.technical_indicators_pb2 import TRADE_ACTION_BUY, TRADE_ACTION_NONE, TRADE_ACTION_SELL, \
    TRADE_ACTION_STRONG_BUY, TRADE_ACTION_STRONG_SELL
from market_analytics_services.market_indicators.indicators_enums import TradeActionColumn, DataColumn, OneChannelColumn


def RoC(data: pd.DataFrame,
        period: int,
        start_date: Optional[pd.Timestamp] = None) -> pd.DataFrame:
    indicator_df = pd.DataFrame(data[DataColumn.DATE].iloc[period:])
    indicator_df.columns = [TradeActionColumn.DATE]
    indicator_df[TradeActionColumn.ACTION] = TRADE_ACTION_NONE
    indicator_df[OneChannelColumn.VALUE] = roc(data[DataColumn.CLOSE], period)
    roc_trade_strategy(indicator_df)
    if start_date is None:
        return indicator_df
    else:
        return indicator_df.loc[start_date:]


def roc_trade_strategy(roc_df: pd.DataFrame):
    roc_mean = roc_df[OneChannelColumn.VALUE].rolling(30).mean()
    roc = roc_df[OneChannelColumn.VALUE].iloc[29:]
    diff = roc - roc_mean
    action = TradeActionColumn.ACTION
    roc_df.loc[diff > 5, action] = TRADE_ACTION_SELL
    roc_df.loc[diff < -5, action] = TRADE_ACTION_BUY
    roc_df.loc[diff >= 10, action] = TRADE_ACTION_STRONG_SELL
    roc_df.loc[diff <= -10, action] = TRADE_ACTION_STRONG_BUY
