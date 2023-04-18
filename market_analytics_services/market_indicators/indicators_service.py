from typing import Dict, Optional, List

from grpc_pbs.technical_indicators_pb2_grpc import TechnicalIndicatorsServicer
from grpc_pbs.technical_indicators_pb2 import SMARequest, EMARequest, WMARequest, RoCRequest, MACDRequest, \
    RSIRequest, AlligatorRequest, BollingerBandsRequest, RVIRequest, \
    RVIResponse, AlligatorResponse, MACDResponse, BollingerBandsResponse, \
    IndicatorBase, OneChannelIndicatorResponse, TradeAction, IndicatorGeneralInfo
from grpc_pbs.technical_indicators_pb2 import TRADE_ACTION_BUY, TRADE_ACTION_NONE, TRADE_ACTION_SELL, \
    TRADE_ACTION_STRONG_BUY, TRADE_ACTION_STRONG_SELL
from google.protobuf.timestamp_pb2 import Timestamp

import psycopg2
import pandas as pd

from market_analytics_services.market_indicators.indicators.alligator import Alligator
from market_analytics_services.market_indicators.indicators.bollinger_bands import BollingerBands
from market_analytics_services.market_indicators.indicators.macd import MACD
from market_analytics_services.market_indicators.indicators.rate_of_change import RoC
from market_analytics_services.market_indicators.indicators.rsi import RSI
from market_analytics_services.market_indicators.indicators.rvi import RVI
from market_analytics_services.market_indicators.indicators_enums import *
from market_analytics_services.market_indicators.indicators.moving_averages import SMA, EMA, WMA


class IndicatorsService(TechnicalIndicatorsServicer):

    def __init__(self, conn: psycopg2._psycopg.connection):
        self.conn = conn
        self.symbols_sources: Dict[str, List[str]] = {}
        with self.conn.cursor() as cursor:
            cursor.execute('SELECT DISTINCT ticker FROM yahoofinance_historical_data')
            self.symbols_sources["yahoofinance_historical_data"] = [ticker[0] for ticker in cursor.fetchall()]
            cursor.execute('SELECT DISTINCT ticker FROM tradingview_tickers_data')
            self.symbols_sources["tradingview_tickers_data"] = [ticker[0] for ticker in cursor.fetchall()]

    def _load_data(self, data_specifics: IndicatorBase) -> pd.DataFrame:
        symbol = data_specifics.symbol
        end_date = data_specifics.end_date.ToDatetime()
        if symbol in self.symbols_sources["yahoofinance_historical_data"]:
            source = "yahoofinance_historical_data"
        elif symbol in self.symbols_sources["tradingview_tickers_data"]:
            source = "tradingview_tickers_data"
        else:
            raise ValueError(f"Database does not contain provided symbol: {symbol}")
        with self.conn.cursor() as cursor:
            if end_date is None:
                cursor.execute(f"""SELECT date::date,
                                 (MIN(ARRAY[id, (open)::float8]))[2] AS open,
                                 (MAX(ARRAY[id, (close)::float8]))[2] AS close,
                                 MAX(high), MIN(low) FROM {source}
                                 WHERE ticker = '{symbol}'
                                 GROUP BY date::date
                                 ORDER BY date::date ASC""")
            else:
                cursor.execute(f"""SELECT date::date,
                 (MIN(ARRAY[id, (open)::float8]))[2] AS open,
                 (MAX(ARRAY[id, (close)::float8]))[2] AS close,
                 MAX(high), MIN(low) FROM {source}
                 WHERE ticker = '{symbol}' AND date::date <= '{end_date}'
                 GROUP BY date::date
                 ORDER BY date::date ASC""")
            df = pd.DataFrame(cursor.fetchall(), columns=DataColumn)
            df.index = df[DataColumn.DATE]
            return df

    def GetSMA(self, request: SMARequest, context) -> OneChannelIndicatorResponse:
        start_date = request.base.start_date.ToDatetime()
        try:
            data = self._load_data(request.base)
            indicator_df = SMA(data, request.period, start_date)
            dates = [Timestamp() for _ in indicator_df[TradeActionColumn.DATE]]
            for i, date in enumerate(indicator_df[TradeActionColumn.DATE]):
                dates[i].FromDatetime(date)
            return OneChannelIndicatorResponse(info=IndicatorGeneralInfo(success=True,
                                                                         error_msg="",
                                                                         dates=dates,
                                                                         recommended_trade_action=indicator_df[
                                                                             TradeActionColumn.ACTION].tolist()),
                                               values=indicator_df[OneChannelColumn.VALUE].tolist())
        except Exception as err:
            return OneChannelIndicatorResponse(info=IndicatorGeneralInfo(success=False,
                                                                         error_msg=err.__str__(),
                                                                         dates=[],
                                                                         recommended_trade_action=[]),
                                               values=[])

    def GetEMA(self, request: EMARequest, context) -> OneChannelIndicatorResponse:
        start_date = request.base.start_date.ToDatetime()
        try:
            data = self._load_data(request.base)
            indicator_df = EMA(data, request.period, request.smoothing_factor, start_date)
            dates = [Timestamp() for _ in indicator_df[TradeActionColumn.DATE]]
            for i, date in enumerate(indicator_df[TradeActionColumn.DATE]):
                dates[i].FromDatetime(date)
            return OneChannelIndicatorResponse(info=IndicatorGeneralInfo(success=True,
                                                                         error_msg="",
                                                                         dates=dates,
                                                                         recommended_trade_action=indicator_df[
                                                                             TradeActionColumn.ACTION].tolist()),
                                               values=indicator_df[OneChannelColumn.VALUE].tolist())
        except Exception as err:
            return OneChannelIndicatorResponse(info=IndicatorGeneralInfo(success=False,
                                                                         error_msg=err.__str__(),
                                                                         dates=[],
                                                                         recommended_trade_action=[]),
                                               values=[])

    def GetWMA(self, request: WMARequest, context) -> OneChannelIndicatorResponse:
        start_date = request.base.start_date.ToDatetime()
        try:
            data = self._load_data(request.base)
            indicator_df = WMA(data, request.period, start_date)
            dates = [Timestamp() for _ in indicator_df[TradeActionColumn.DATE]]
            for i, date in enumerate(indicator_df[TradeActionColumn.DATE]):
                dates[i].FromDatetime(date)
            return OneChannelIndicatorResponse(info=IndicatorGeneralInfo(success=True,
                                                                         error_msg="",
                                                                         dates=dates,
                                                                         recommended_trade_action=indicator_df[
                                                                             TradeActionColumn.ACTION].tolist()),
                                               values=indicator_df[OneChannelColumn.VALUE].tolist())
        except Exception as err:
            return OneChannelIndicatorResponse(info=IndicatorGeneralInfo(success=False,
                                                                         error_msg=err.__str__(),
                                                                         dates=[],
                                                                         recommended_trade_action=[]),
                                               values=[])

    def GetRoC(self, request: RoCRequest, context) -> OneChannelIndicatorResponse:
        start_date = request.base.start_date.ToDatetime()
        try:
            data = self._load_data(request.base)
            indicator_df = RoC(data, request.period, start_date)
            dates = [Timestamp() for _ in indicator_df[TradeActionColumn.DATE]]
            for i, date in enumerate(indicator_df[TradeActionColumn.DATE]):
                dates[i].FromDatetime(date)
            return OneChannelIndicatorResponse(info=IndicatorGeneralInfo(success=True,
                                                                         error_msg="",
                                                                         dates=dates,
                                                                         recommended_trade_action=indicator_df[
                                                                             TradeActionColumn.ACTION].tolist()),
                                               values=indicator_df[OneChannelColumn.VALUE].tolist())
        except Exception as err:
            return OneChannelIndicatorResponse(info=IndicatorGeneralInfo(success=False,
                                                                         error_msg=err.__str__(),
                                                                         dates=[],
                                                                         recommended_trade_action=[]),
                                               values=[])

    def GetMACD(self, request: MACDRequest, context) -> MACDResponse:
        start_date = request.base.start_date.ToDatetime()
        try:
            data = self._load_data(request.base)
            indicator_df = MACD(data, request.fast_period, request.slow_period, request.signal_period, start_date)
            dates = [Timestamp() for _ in indicator_df[TradeActionColumn.DATE]]
            for i, date in enumerate(indicator_df[TradeActionColumn.DATE]):
                dates[i].FromDatetime(date)
            return MACDResponse(info=IndicatorGeneralInfo(success=True,
                                                          error_msg="",
                                                          dates=dates,
                                                          recommended_trade_action=indicator_df[
                                                              TradeActionColumn.ACTION].tolist()),
                                macd=indicator_df[MACDColumn.MACD].tolist(),
                                signal=indicator_df[MACDColumn.SIGNAL].tolist(),
                                diff=indicator_df[MACDColumn.DIFF])
        except Exception as err:
            return MACDResponse(info=IndicatorGeneralInfo(success=False,
                                                          error_msg=err.__str__(),
                                                          dates=[],
                                                          recommended_trade_action=[]),
                                macd=[],
                                signal=[],
                                diff=[])

    def GetRSI(self, request: RSIRequest, context) -> OneChannelIndicatorResponse:
        start_date = request.base.start_date.ToDatetime()
        try:
            data = self._load_data(request.base)
            indicator_df = RSI(data, request.period, start_date)
            dates = [Timestamp() for _ in indicator_df[TradeActionColumn.DATE]]
            for i, date in enumerate(indicator_df[TradeActionColumn.DATE]):
                dates[i].FromDatetime(date)
            return OneChannelIndicatorResponse(info=IndicatorGeneralInfo(success=True,
                                                                         error_msg="",
                                                                         dates=dates,
                                                                         recommended_trade_action=indicator_df[
                                                                             TradeActionColumn.ACTION].tolist()),
                                               values=indicator_df[OneChannelColumn.VALUE].tolist())
        except Exception as err:
            return OneChannelIndicatorResponse(info=IndicatorGeneralInfo(success=False,
                                                                         error_msg=err.__str__(),
                                                                         dates=[],
                                                                         recommended_trade_action=[]),
                                               values=[])

    def GetAlligator(self, request: AlligatorRequest, context) -> AlligatorResponse:
        start_date = request.base.start_date.ToDatetime()
        try:
            data = self._load_data(request.base)
            indicator_df = Alligator(data, start_date)
            dates = [Timestamp() for _ in indicator_df[TradeActionColumn.DATE]]
            for i, date in enumerate(indicator_df[TradeActionColumn.DATE]):
                dates[i].FromDatetime(date)
            return AlligatorResponse(info=IndicatorGeneralInfo(success=True,
                                                               error_msg="",
                                                               dates=dates,
                                                               recommended_trade_action=indicator_df[
                                                                   TradeActionColumn.ACTION].tolist()),
                                     lips=indicator_df[AlligatorColumn.LIPS].tolist(),
                                     teeth=indicator_df[AlligatorColumn.TEETH].tolist(),
                                     jaw=indicator_df[AlligatorColumn.JAW].tolist())
        except Exception as err:
            return AlligatorResponse(info=IndicatorGeneralInfo(success=False,
                                                               error_msg=err.__str__(),
                                                               dates=[],
                                                               recommended_trade_action=[]),
                                     lips=[],
                                     teeth=[],
                                     jaw=[])

    def GetBollingerBands(self, request: BollingerBandsRequest, context) -> BollingerBandsResponse:
        start_date = request.base.start_date.ToDatetime()
        try:
            data = self._load_data(request.base)
            indicator_df = BollingerBands(data, request.ma_period, request.width_factor, start_date)
            dates = [Timestamp() for _ in indicator_df[TradeActionColumn.DATE]]
            for i, date in enumerate(indicator_df[TradeActionColumn.DATE]):
                dates[i].FromDatetime(date)
            return BollingerBandsResponse(info=IndicatorGeneralInfo(success=True,
                                                                    error_msg="",
                                                                    dates=dates,
                                                                    recommended_trade_action=indicator_df[
                                                                        TradeActionColumn.ACTION].tolist()),
                                          lower_band=indicator_df[BollingerBandsColumn.LOWER_BAND].tolist(),
                                          ma=indicator_df[BollingerBandsColumn.MA].tolist(),
                                          upper_band=indicator_df[BollingerBandsColumn.UPPER_BAND].tolist())
        except Exception as err:
            return BollingerBandsResponse(info=IndicatorGeneralInfo(success=False,
                                                                    error_msg=err.__str__(),
                                                                    dates=[],
                                                                    recommended_trade_action=[]),
                                          lower_band=[],
                                          ma=[],
                                          upper_band=[])

    def GetRVI(self, request: RVIRequest, context) -> RVIResponse:
        start_date = request.base.start_date.ToDatetime()
        try:
            data = self._load_data(request.base)
            indicator_df = RVI(data, request.smoothing_period, request.signal_period, start_date)
            dates = [Timestamp() for _ in indicator_df[TradeActionColumn.DATE]]
            for i, date in enumerate(indicator_df[TradeActionColumn.DATE]):
                dates[i].FromDatetime(date)
            return RVIResponse(info=IndicatorGeneralInfo(success=True,
                                                         error_msg="",
                                                         dates=dates,
                                                         recommended_trade_action=indicator_df[
                                                             TradeActionColumn.ACTION].tolist()),
                               rvi=indicator_df[RVIColumn.RVI].tolist(),
                               signal=indicator_df[RVIColumn.SIGNAL].tolist())
        except Exception as err:
            return RVIResponse(info=IndicatorGeneralInfo(success=False,
                                                         error_msg=err.__str__(),
                                                         dates=[],
                                                         recommended_trade_action=[]),
                               rvi=[],
                               signal=[])


if __name__ == "__main__":
    conn = psycopg2.connect(dbname='politehdb',
                            user='politeh',
                            password='RxKWF20V6f0K',
                            host='188.120.230.134',
                            port='5432')
    cursor = conn.cursor()
    cursor.execute('SELECT DISTINCT ticker FROM yahoofinance_historical_data')
    yahoo_tickers = cursor.fetchall()
    cursor.execute("""
        SELECT DISTINCT ticker FROM tradingview_tickers_data
        EXCEPT
        SELECT DISTINCT ticker FROM yahoofinance_historical_data""")
    trading_view_tickers = cursor.fetchall()
    symbols_dict: Dict[str, pd.DataFrame] = {}
    for symbol in yahoo_tickers:
        cursor.execute(f"""
                SELECT date, open, close, high, low FROM yahoofinance_historical_data
                WHERE ticker = '{symbol[0]}'
                ORDER BY date ASC""")
        df = pd.DataFrame(cursor.fetchall(), columns=DataColumn)
        df.index = df[DataColumn.DATE]
        symbols_dict[symbol[0]] = df
    for symbol in trading_view_tickers:
        cursor.execute(f"""
                SELECT date, open, close, high, low FROM tradingview_tickers_data
                WHERE ticker = '{symbol[0]}'
                ORDER BY date ASC""")
        df = pd.DataFrame(cursor.fetchall(), columns=DataColumn)
        df.index = df[DataColumn.DATE]
        symbols_dict[symbol[0]] = df
    cursor.close()
    conn.close()
    a = 1
