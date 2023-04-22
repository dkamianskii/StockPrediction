from typing import Optional
import pandas as pd

from grpc_pbs.technical_indicators_pb2 import TRADE_ACTION_BUY, TRADE_ACTION_NONE, TRADE_ACTION_SELL, \
    TRADE_ACTION_STRONG_BUY, TRADE_ACTION_STRONG_SELL
from market_analytics_services.market_indicators.indicators_enums import TradeActionColumn, DataColumn, OneChannelColumn

from datetime import date


def SMA(data: pd.DataFrame,
        period: int,
        start_date: Optional[date] = None) -> pd.DataFrame:
    indicator_df = pd.DataFrame(data[DataColumn.DATE])
    indicator_df.columns = [TradeActionColumn.DATE]
    indicator_df[TradeActionColumn.ACTION] = TRADE_ACTION_NONE
    indicator_df[OneChannelColumn.VALUE] = data[DataColumn.CLOSE].rolling(period).mean()
    indicator_df.dropna(inplace=True)
    if start_date is None:
        return indicator_df
    else:
        return indicator_df.loc[start_date:]


def EMA(data: pd.DataFrame,
        period: int,
        smoothing_factor: Optional[float],
        start_date: Optional[date] = None) -> pd.DataFrame:
    indicator_df = pd.DataFrame(data[DataColumn.DATE])
    indicator_df.columns = [TradeActionColumn.DATE]
    indicator_df[TradeActionColumn.ACTION] = TRADE_ACTION_NONE
    if smoothing_factor is None:
        indicator_df[OneChannelColumn.VALUE] = data[DataColumn.CLOSE].ewm(span=period, adjust=False).mean()
    else:
        indicator_df[OneChannelColumn.VALUE] = data[DataColumn.CLOSE].ewm(alpha=smoothing_factor, adjust=False).mean()
    if start_date is None:
        return indicator_df
    else:
        return indicator_df.loc[start_date:]


def WMA(data: pd.DataFrame,
        period: int,
        start_date: Optional[date] = None) -> pd.DataFrame:
    indicator_df = pd.DataFrame(data[DataColumn.DATE])
    indicator_df.columns = [TradeActionColumn.DATE]
    indicator_df[TradeActionColumn.ACTION] = TRADE_ACTION_NONE
    base = period * (period + 1) / 2
    weights = [i / base for i in range(1, period + 1)]
    indicator_df[OneChannelColumn.VALUE] = data[DataColumn.CLOSE].rolling(period).apply(lambda x: (x * weights).sum())
    indicator_df.dropna(inplace=True)
    if start_date is None:
        return indicator_df
    else:
        return indicator_df.loc[start_date:]



