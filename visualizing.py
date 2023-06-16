from typing import Optional

from grpc_pbs.technical_indicators_pb2 import TRADE_ACTION_BUY, TRADE_ACTION_NONE, TRADE_ACTION_SELL, \
    TRADE_ACTION_STRONG_BUY, TRADE_ACTION_STRONG_SELL
from market_analytics_services.market_indicators.indicators_enums import *

import pandas as pd
import numpy as np
import cufflinks as cf
from plotly.subplots import make_subplots
import plotly.graph_objects as go

cf.go_offline()


def plot_rsi(data: pd.DataFrame, indicator_df: pd.DataFrame, img_dir: str, name: str):
    fig = make_subplots(rows=2, cols=1,
                        shared_xaxes=True,
                        vertical_spacing=0.2)

    fig.add_candlestick(x=data.index,
                        open=data[DataColumn.OPEN],
                        close=data[DataColumn.CLOSE],
                        high=data[DataColumn.HIGH],
                        low=data[DataColumn.LOW],
                        name="Price",
                        row=1, col=1)

    action = indicator_df[indicator_df[TradeActionColumn.ACTION] != TRADE_ACTION_NONE]
    action_price = data.loc[action[TradeActionColumn.DATE]][DataColumn.CLOSE]
    bool_buys = action[TradeActionColumn.ACTION].isin([TRADE_ACTION_BUY, TRADE_ACTION_STRONG_BUY])
    actives = action[TradeActionColumn.ACTION].isin([TRADE_ACTION_STRONG_BUY, TRADE_ACTION_STRONG_SELL])
    fig.add_trace(go.Scatter(x=action[TradeActionColumn.DATE],
                             y=action_price,
                             mode="markers",
                             marker=dict(
                                 color=np.where(bool_buys, "green", "red"),
                                 size=np.where(actives, 15, 10),
                                 symbol=np.where(bool_buys, "triangle-up", "triangle-down")),
                             name="Action points"),
                  row=1, col=1)

    fig.add_trace(go.Scatter(x=indicator_df[TradeActionColumn.DATE], y=indicator_df[OneChannelColumn.VALUE], mode='lines',
                             line=dict(width=1, color="blue"), name="RSI"),
                  row=2, col=1)
    fig.add_trace(go.Scatter(x=indicator_df[TradeActionColumn.DATE], y=np.full(indicator_df.shape[0], 70), mode='lines',
                             line=dict(width=1, dash='dash', color="black"), showlegend=False),
                  row=2, col=1)
    fig.add_trace(go.Scatter(x=indicator_df[TradeActionColumn.DATE], y=np.full(indicator_df.shape[0], 30), mode='lines',
                             line=dict(width=1, dash='dash', color="black"), showlegend=False),
                  row=2, col=1)

    fig.update_layout(title=f"{name} with RSI",
                      xaxis_title="Date")

    #fig.show()
    fig.write_image(f"{img_dir}/rsi.png", scale=1, width=1400, height=900)


def plot_roc(data: pd.DataFrame, indicator_df: pd.DataFrame, img_dir: str, name: str):
    fig = make_subplots(rows=2, cols=1,
                        shared_xaxes=True,
                        vertical_spacing=0.2)

    fig.add_candlestick(x=data.index,
                        open=data[DataColumn.OPEN],
                        close=data[DataColumn.CLOSE],
                        high=data[DataColumn.HIGH],
                        low=data[DataColumn.LOW],
                        name="Price",
                        row=1, col=1)

    action = indicator_df[indicator_df[TradeActionColumn.ACTION] != TRADE_ACTION_NONE]
    action_price = data.loc[action[TradeActionColumn.DATE]][DataColumn.CLOSE]
    bool_buys = action[TradeActionColumn.ACTION].isin([TRADE_ACTION_BUY, TRADE_ACTION_STRONG_BUY])
    actives = action[TradeActionColumn.ACTION].isin([TRADE_ACTION_STRONG_BUY, TRADE_ACTION_STRONG_SELL])
    fig.add_trace(go.Scatter(x=action[TradeActionColumn.DATE],
                             y=action_price,
                             mode="markers",
                             marker=dict(
                                 color=np.where(bool_buys, "green", "red"),
                                 size=np.where(actives, 15, 10),
                                 symbol=np.where(bool_buys, "triangle-up", "triangle-down")),
                             name="Action points"),
                  row=1, col=1)

    fig.add_trace(go.Scatter(x=indicator_df[TradeActionColumn.DATE], y=indicator_df[OneChannelColumn.VALUE], mode='lines',
                             line=dict(width=1, color="blue"), name="RoC"),
                  row=2, col=1)

    fig.update_layout(title=f"{name} with RoC",
                      xaxis_title="Date")

    #fig.show()
    fig.write_image(f"{img_dir}/roc.png", scale=1, width=1400, height=900)


def plot_macd(data: pd.DataFrame, indicator_df: pd.DataFrame, img_dir: str, name: str):
    fig = make_subplots(rows=2, cols=1,
                        shared_xaxes=True,
                        vertical_spacing=0.2)

    fig.add_candlestick(x=data.index,
                        open=data[DataColumn.OPEN],
                        close=data[DataColumn.CLOSE],
                        high=data[DataColumn.HIGH],
                        low=data[DataColumn.LOW],
                        name="Price",
                        row=1, col=1)

    action = indicator_df[indicator_df[TradeActionColumn.ACTION] != TRADE_ACTION_NONE]
    action_price = data.loc[action[TradeActionColumn.DATE]][DataColumn.CLOSE]
    bool_buys = action[TradeActionColumn.ACTION].isin([TRADE_ACTION_BUY, TRADE_ACTION_STRONG_BUY])
    actives = action[TradeActionColumn.ACTION].isin([TRADE_ACTION_STRONG_BUY, TRADE_ACTION_STRONG_SELL])
    fig.add_trace(go.Scatter(x=action[TradeActionColumn.DATE],
                             y=action_price,
                             mode="markers",
                             marker=dict(
                                 color=np.where(bool_buys, "green", "red"),
                                 size=np.where(actives, 15, 10),
                                 symbol=np.where(bool_buys, "triangle-up", "triangle-down")),
                             name="Action points"),
                  row=1, col=1)

    fig.add_trace(go.Scatter(x=indicator_df[TradeActionColumn.DATE], y=indicator_df[MACDColumn.MACD], mode='lines',
                             line=dict(width=1, color="blue"), name="MACD"),
                  row=2, col=1)
    fig.add_trace(go.Scatter(x=indicator_df[TradeActionColumn.DATE], y=indicator_df[MACDColumn.SIGNAL], mode='lines',
                             line=dict(width=1, color="orange"), name="signal line"),
                  row=2, col=1)

    fig.add_bar(x=indicator_df[TradeActionColumn.DATE], y=indicator_df[MACDColumn.DIFF], marker=dict(
        color=np.where(indicator_df[MACDColumn.DIFF] > 0, "green", "red")
    ), name="MACD signal difference", row=2, col=1)

    fig.update_layout(title=f"{name} with MACD",
                      xaxis_title="Date")

    #fig.show()
    fig.write_image(f"{img_dir}/macd.png", scale=1, width=1400, height=900)


def plot_rvi(data: pd.DataFrame, indicator_df: pd.DataFrame, img_dir: str, name: str):
    fig = make_subplots(rows=2, cols=1,
                        shared_xaxes=True,
                        vertical_spacing=0.2)

    fig.add_candlestick(x=data.index,
                        open=data[DataColumn.OPEN],
                        close=data[DataColumn.CLOSE],
                        high=data[DataColumn.HIGH],
                        low=data[DataColumn.LOW],
                        name="Price",
                        row=1, col=1)

    action = indicator_df[indicator_df[TradeActionColumn.ACTION] != TRADE_ACTION_NONE]
    action_price = data.loc[action[TradeActionColumn.DATE]][DataColumn.CLOSE]
    bool_buys = action[TradeActionColumn.ACTION].isin([TRADE_ACTION_BUY, TRADE_ACTION_STRONG_BUY])
    actives = action[TradeActionColumn.ACTION].isin([TRADE_ACTION_STRONG_BUY, TRADE_ACTION_STRONG_SELL])
    fig.add_trace(go.Scatter(x=action[TradeActionColumn.DATE],
                             y=action_price,
                             mode="markers",
                             marker=dict(
                                 color=np.where(bool_buys, "green", "red"),
                                 size=np.where(actives, 15, 10),
                                 symbol=np.where(bool_buys, "triangle-up", "triangle-down")),
                             name="Action points"),
                  row=1, col=1)

    fig.add_trace(go.Scatter(x=indicator_df[TradeActionColumn.DATE], y=indicator_df[RVIColumn.RVI], mode='lines',
                             line=dict(width=1, color="blue"), name="RVI"),
                  row=2, col=1)
    fig.add_trace(go.Scatter(x=indicator_df[TradeActionColumn.DATE], y=indicator_df[RVIColumn.SIGNAL], mode='lines',
                             line=dict(width=1, color="orange"), name="signal line"),
                  row=2, col=1)

    fig.update_layout(title=f"{name} with RVI",
                      xaxis_title="Date")

    #fig.show()
    fig.write_image(f"{img_dir}/rvi.png", scale=1, width=1400, height=900)


def plot_bollinger(data: pd.DataFrame, indicator_df: pd.DataFrame, img_dir: str, name: str):
    fig = go.Figure()
    fig.add_candlestick(x=data.index,
                        open=data[DataColumn.OPEN],
                        close=data[DataColumn.CLOSE],
                        high=data[DataColumn.HIGH],
                        low=data[DataColumn.LOW],
                        name="Price")

    fig.add_trace(go.Scatter(x=indicator_df[TradeActionColumn.DATE], y=indicator_df[BollingerBandsColumn.LOWER_BAND],
                             mode='lines', line=dict(width=1, color="orange"), name="Lower band"))

    fig.add_trace(go.Scatter(x=indicator_df[TradeActionColumn.DATE], y=indicator_df[BollingerBandsColumn.UPPER_BAND],
                             mode='lines', line=dict(width=1, color="blue"), name="Upper band", fill='tonexty'))

    action = indicator_df[indicator_df[TradeActionColumn.ACTION] != TRADE_ACTION_NONE]
    action_price = data.loc[action[TradeActionColumn.DATE]][DataColumn.CLOSE]
    bool_buys = action[TradeActionColumn.ACTION].isin([TRADE_ACTION_BUY, TRADE_ACTION_STRONG_BUY])
    actives = action[TradeActionColumn.ACTION].isin([TRADE_ACTION_STRONG_BUY, TRADE_ACTION_STRONG_SELL])
    fig.add_trace(go.Scatter(x=action[TradeActionColumn.DATE],
                             y=action_price,
                             mode="markers",
                             marker=dict(
                                 color=np.where(bool_buys, "green", "red"),
                                 size=np.where(actives, 15, 10),
                                 symbol=np.where(bool_buys, "triangle-up", "triangle-down")),
                             name="Action points"))

    fig.update_layout(title=f"{name} with Bollinger bands",
                      xaxis_title="Date",
                      yaxis_title="Price")

    #fig.show()
    fig.write_image(f"{img_dir}/bollinger.png", scale=1, width=1400, height=900)


def plot_alligator(data: pd.DataFrame, indicator_df: pd.DataFrame, img_dir: str, name: str):
    fig = go.Figure()
    fig.add_candlestick(x=data.index,
                        open=data[DataColumn.OPEN],
                        close=data[DataColumn.CLOSE],
                        high=data[DataColumn.HIGH],
                        low=data[DataColumn.LOW],
                        name="Price")

    fig.add_trace(go.Scatter(x=indicator_df[TradeActionColumn.DATE], y=indicator_df[AlligatorColumn.LIPS],
                             mode='lines', line=dict(width=1, color="green"), name="Lower band"))

    fig.add_trace(go.Scatter(x=indicator_df[TradeActionColumn.DATE], y=indicator_df[AlligatorColumn.TEETH],
                             mode='lines', line=dict(width=1, color="red"), name="Upper band"))

    fig.add_trace(go.Scatter(x=indicator_df[TradeActionColumn.DATE], y=indicator_df[AlligatorColumn.JAW],
                             mode='lines', line=dict(width=1, color="blue"), name="Upper band"))

    action = indicator_df[indicator_df[TradeActionColumn.ACTION] != TRADE_ACTION_NONE]
    action_price = data.loc[action[TradeActionColumn.DATE]][DataColumn.CLOSE]
    bool_buys = action[TradeActionColumn.ACTION].isin([TRADE_ACTION_BUY, TRADE_ACTION_STRONG_BUY])
    actives = action[TradeActionColumn.ACTION].isin([TRADE_ACTION_STRONG_BUY, TRADE_ACTION_STRONG_SELL])
    fig.add_trace(go.Scatter(x=action[TradeActionColumn.DATE],
                             y=action_price,
                             mode="markers",
                             marker=dict(
                                 color=np.where(bool_buys, "green", "red"),
                                 size=np.where(actives, 15, 10),
                                 symbol=np.where(bool_buys, "triangle-up", "triangle-down")),
                             name="Action points"))

    fig.update_layout(title=f"{name} with Alligator",
                      xaxis_title="Date",
                      yaxis_title="Price")

    #fig.show()
    fig.write_image(f"{img_dir}/alligator.png", scale=1, width=1400, height=900)