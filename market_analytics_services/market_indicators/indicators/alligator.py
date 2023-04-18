from typing import Optional

import numpy as np
import pandas as pd
from enum import Enum


from grpc_pbs.technical_indicators_pb2 import TRADE_ACTION_BUY, TRADE_ACTION_NONE, TRADE_ACTION_SELL, \
    TRADE_ACTION_STRONG_BUY, TRADE_ACTION_STRONG_SELL
from market_analytics_services.market_indicators.indicators_enums import TradeActionColumn, DataColumn, AlligatorColumn


def Alligator(data: pd.DataFrame,
        start_date: Optional[pd.Timestamp] = None) -> pd.DataFrame:
    indicator_df = pd.DataFrame(data[DataColumn.DATE])
    indicator_df.columns = [TradeActionColumn.DATE]
    indicator_df[TradeActionColumn.ACTION] = TRADE_ACTION_NONE
    median_price = data[DataColumn.HIGH] + data[DataColumn.LOW]
    indicator_df[AlligatorColumn.JAW] = SMMA(median_price, 13, 8)
    indicator_df[AlligatorColumn.TEETH] = SMMA(median_price, 8, 5)
    indicator_df[AlligatorColumn.LIPS] = SMMA(median_price, 5, 3)
    indicator_df.dropna(inplace=True)
    alligator_trade_strategy(ali_df=indicator_df, price=data[DataColumn.CLOSE])
    if start_date is None:
        return indicator_df
    else:
        return indicator_df.loc[start_date:]


class State(Enum):
    SLEEP = 0
    EATING_BULL = 1
    EATING_BEAR = 2


def get_state(lips, teeth, jaw):
    lips_teeth_diff = lips - teeth
    jaw_teeth_diff = jaw - teeth
    if lips_teeth_diff > 0 > jaw_teeth_diff:
        return State.EATING_BULL
    elif lips_teeth_diff < 0 < jaw_teeth_diff:
        return State.EATING_BEAR
    return State.SLEEP


def alligator_trade_strategy(ali_df: pd.DataFrame, price: pd.Series):
    action = TradeActionColumn.ACTION
    fst = ali_df.iloc[0]
    prev_state = get_state(fst[AlligatorColumn.LIPS], fst[AlligatorColumn.TEETH], fst[AlligatorColumn.JAW])
    start_price = price.loc[fst[TradeActionColumn.DATE]]
    mouth_open = False
    eating_days = 0
    prey_width = 0
    sleeping_days = 0
    expected_prey = 0
    for index, row in ali_df[1:].iterrows():
        state = get_state(row[AlligatorColumn.LIPS], row[AlligatorColumn.TEETH], row[AlligatorColumn.JAW])
        if sleeping_days != 0:
            sleeping_days -= 1
            prev_state = state
            continue
        if state != State.SLEEP and prev_state == State.SLEEP:
            mouth_open = True
        if mouth_open:
            if state == State.SLEEP:
                mouth_open = False
                if eating_days != 0:
                    price_diff = price.loc[row[TradeActionColumn.DATE]] - start_price
                    prey_width /= eating_days
                    if (prev_state == State.EATING_BULL and price_diff > 0) \
                            or (prev_state == State.EATING_BEAR and price_diff < 0):
                        expected_prey = 0.75 * prey_width + 0.25 * expected_prey
                        sleeping_days = int(eating_days / 4)
                        eating_days = 0
            else:
                curr_width = np.abs(row[AlligatorColumn.LIPS] - row[AlligatorColumn.JAW])
                if eating_days == 0 and curr_width >= 0.8 * expected_prey:
                    if state == State.EATING_BULL:
                        ali_df.loc[row[TradeActionColumn.DATE], action] = TRADE_ACTION_BUY
                    else:
                        ali_df.loc[row[TradeActionColumn.DATE], action] = TRADE_ACTION_SELL
                    eating_days = 1
                    start_price = price.loc[row[TradeActionColumn.DATE]]
                    prey_width = curr_width
                elif eating_days != 0:
                    eating_days += 1
                    prey_width += curr_width
        else:
            expected_prey *= 0.975


def SMMA(x, N, S) -> pd.Series:
    new_x = x.copy()
    new_x[:N - 1] = np.NAN
    new_x[N - 1] = np.mean(x[:N])
    return new_x.ewm(alpha=1/N, adjust=False, ignore_na=True).shift(S)
