from typing import Optional

import numpy as np
import pandas as pd
from ta.volatility import bollinger_hband, bollinger_lband, bollinger_mavg

from grpc_pbs.technical_indicators_pb2 import TRADE_ACTION_BUY, TRADE_ACTION_NONE, TRADE_ACTION_SELL, \
    TRADE_ACTION_STRONG_BUY, TRADE_ACTION_STRONG_SELL
from market_analytics_services.market_indicators.indicators_enums import TradeActionColumn, DataColumn, BollingerBandsColumn
from datetime import date


def BollingerBands(data: pd.DataFrame,
                   ma_period: Optional[int] = None,
                   width_factor: Optional[int] = None,
                   start_date: Optional[date] = None) -> pd.DataFrame:
    ma_period = 20 if ma_period is None else ma_period
    width_factor = 2 if width_factor is None else width_factor
    indicator_df = pd.DataFrame(data[DataColumn.DATE])
    indicator_df.columns = [TradeActionColumn.DATE]
    indicator_df[TradeActionColumn.ACTION] = TRADE_ACTION_NONE
    indicator_df[BollingerBandsColumn.UPPER_BAND] = bollinger_hband(data[DataColumn.CLOSE], ma_period, width_factor)
    indicator_df[BollingerBandsColumn.LOWER_BAND] = bollinger_lband(data[DataColumn.CLOSE], ma_period, width_factor)
    indicator_df[BollingerBandsColumn.MA] = bollinger_mavg(data[DataColumn.CLOSE], ma_period)
    bollinger_bands_strategy(data, indicator_df)
    indicator_df.dropna(inplace=True)
    if start_date is None:
        return indicator_df
    else:
        return indicator_df.loc[start_date:]


def bollinger_bands_strategy(data, bb_df):
    open = data[DataColumn.OPEN]
    close = data[DataColumn.CLOSE]
    up_b = bb_df[BollingerBandsColumn.UPPER_BAND]
    low_b = bb_df[BollingerBandsColumn.LOWER_BAND]
    action = TradeActionColumn.ACTION
    bb_df.loc[(close > up_b) & (close > open), action] = TRADE_ACTION_SELL
    bb_df.loc[(close < low_b) & (close < open), action] = TRADE_ACTION_BUY
    bb_df.loc[(open > up_b) & (close > up_b), action] = TRADE_ACTION_STRONG_SELL
    bb_df.loc[(open < low_b) & (close < low_b), action] = TRADE_ACTION_STRONG_BUY
