import sys
from concurrent import futures

from grpc_pbs.stock_financial_analytics_pb2_grpc import add_StockFinancialAnalyticsServicer_to_server
from base_analytics.financial_analytics_service import StockFinancialAnalyticsService

from grpc_pbs.technical_indicators_pb2_grpc import add_TechnicalIndicatorsServicer_to_server
from market_indicators.indicators_service import IndicatorsService
from config import *

import grpc

import psycopg2


def market_analytics_server(max_workers: int = 10,
                            address_of_port: str = '[::]:50051'):
    conn = psycopg2.connect(dbname='politehdb',
                                 user='politeh',
                                 password='RxKWF20V6f0K',
                                 host='188.120.230.134',
                                 port='5432')
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=max_workers))
    server.add_insecure_port('[::]:50051')
    add_StockFinancialAnalyticsServicer_to_server(StockFinancialAnalyticsService(conn), server)
    add_TechnicalIndicatorsServicer_to_server(IndicatorsService(conn), server)
    server.start()
    print("market analytics server started")
    server.wait_for_termination()


if __name__ == "__main__":
    market_analytics_server(max_workers=MAX_WORKERS, address_of_port=ADRESS_OF_PORT)




