from typing import Optional

import numpy as np
import pandas as pd
from enum import Enum

from grpc_pbs.technical_indicators_pb2 import TRADE_ACTION_BUY, TRADE_ACTION_NONE, TRADE_ACTION_SELL, \
    TRADE_ACTION_STRONG_BUY, TRADE_ACTION_STRONG_SELL
from market_analytics_services.market_indicators.indicators_enums import TradeActionColumn, DataColumn, AlligatorColumn
from datetime import date


def Alligator(data: pd.DataFrame,
              start_date: Optional[date] = None) -> pd.DataFrame:
    indicator_df = pd.DataFrame(data[DataColumn.DATE])
    indicator_df.columns = [TradeActionColumn.DATE]
    indicator_df[TradeActionColumn.ACTION] = TRADE_ACTION_NONE
    median_price = (data[DataColumn.HIGH] + data[DataColumn.LOW]) / 2
    indicator_df[AlligatorColumn.JAW] = SMMA(median_price, 13, 8)
    indicator_df[AlligatorColumn.TEETH] = SMMA(median_price, 8, 5)
    indicator_df[AlligatorColumn.LIPS] = SMMA(median_price, 5, 3)
    indicator_df.dropna(inplace=True)
    alligator_trade_strategy(ali_df=indicator_df, close=data[DataColumn.CLOSE])
    if start_date is None:
        return indicator_df
    else:
        return indicator_df.loc[start_date:]


def SMMA(x, N, S) -> pd.Series:
    new_x = x.copy()
    new_x[:N - 1] = np.NAN
    new_x[N - 1] = np.mean(x[:N])
    return new_x.ewm(alpha=1 / N, adjust=False, ignore_na=True).mean().shift(S)


class State(Enum):
    NONE = 1
    LONG = 2
    SHORT = 3


def alligator_trade_strategy(ali_df: pd.DataFrame, close: pd.Series):
    action = TradeActionColumn.ACTION
    state = State.NONE
    for index, row in ali_df.iterrows():
        lips, teeth, jaw = row[[AlligatorColumn.LIPS, AlligatorColumn.TEETH, AlligatorColumn.JAW]]
        if state == State.SHORT:
            if close[index] >= lips:
                ali_df.loc[index, action] = TRADE_ACTION_BUY
                state = state.NONE
        elif state == State.LONG:
            if close[index] <= lips:
                ali_df.loc[index, action] = TRADE_ACTION_SELL
                state = state.NONE
        else:
            if np.abs(lips - jaw) / lips >= 0.015:
                if lips > teeth > jaw:
                    if close[index] <= teeth:
                        ali_df.loc[index, action] = TRADE_ACTION_SELL
                        state = State.SHORT
                elif lips < teeth < jaw:
                    if close[index] >= teeth:
                        ali_df.loc[index, action] = TRADE_ACTION_BUY
                        state = State.LONG

