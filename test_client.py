import pandas as pd
import numpy as np

import grpc
import psycopg2

from grpc_pbs.technical_indicators_pb2_grpc import TechnicalIndicatorsStub
from grpc_pbs.technical_indicators_pb2 import SMARequest, IndicatorBase, OneChannelIndicatorResponse
from grpc_pbs.stock_financial_analytics_pb2_grpc import StockFinancialAnalyticsStub
from grpc_pbs.stock_financial_analytics_pb2 import StockAnalysisRequest, StockAnalysisResponse
from google.protobuf.timestamp_pb2 import Timestamp

import datetime

from market_analytics_services.market_indicators.indicators.moving_averages import SMA
from market_analytics_services.market_indicators.indicators.rate_of_change import RoC
from market_analytics_services.market_indicators.indicators.rsi import RSI
from market_analytics_services.market_indicators.indicators_enums import DataColumn


def test_fundamental(stock_symbol: str):
    channel = grpc.insecure_channel("localhost:50051")
    client = StockFinancialAnalyticsStub(channel)
    start_date = datetime.datetime(year=2000, month=1, day=1)
    end_date = datetime.datetime(year=2020, month=1, day=1)
    start_date_t = Timestamp()
    end_date_t = Timestamp()
    start_date_t.FromDatetime(start_date)
    end_date_t.FromDatetime(end_date)
    analytics: StockAnalysisResponse = client.GetAnalytics(StockAnalysisRequest(stock_symbol=stock_symbol,
                                                                                start_year=2000,
                                                                                end_year=2020,
                                                                                language="EN"))
    print(analytics.error_msg)
    print(analytics.analytics)


def test_indicators():
    channel = grpc.insecure_channel("localhost:50051")
    client = TechnicalIndicatorsStub(channel)
    start_date = datetime.datetime(year=2000, month=1, day=1)
    end_date = datetime.datetime(year=2020, month=1, day=1)
    start_date_t = Timestamp()
    end_date_t = Timestamp()
    start_date_t.FromDatetime(start_date)
    end_date_t.FromDatetime(end_date)
    b = IndicatorBase(symbol="Brent Crude Oil Last Day", start_date=start_date_t, end_date=end_date_t)
    request = SMARequest(base=b, period=10)
    sma: OneChannelIndicatorResponse = client.GetSMA(request)
    val = sma.values
    info = sma.info
    print(info.error_msg)
    dates = info.dates
    print(info.recommended_trade_action)
    for i in range(len(val)):
        print(dates[i].ToDatetime().date(), val[i])


def indi():
    conn = psycopg2.connect(dbname='politehdb',
                            user='politeh',
                            password='RxKWF20V6f0K',
                            host='188.120.230.134',
                            port='5432')
    cursor = conn.cursor()
    cursor.execute(f"""
                    SELECT date, open, close, high, low FROM yahoofinance_historical_data
                    WHERE ticker = 'Brent Crude Oil Last Day' AND date::date <= '2019.12.31'
                    ORDER BY date ASC""")
    df = pd.DataFrame(cursor.fetchall(), columns=DataColumn)
    df.index = df[DataColumn.DATE]
    res2 = RSI(df, 14)
    cursor.close()
    conn.close()


if __name__ == "__main__":
    # test_indicators()
    test_fundamental("газпром")
    # indi()
