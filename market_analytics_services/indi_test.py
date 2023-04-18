from grpc_pbs.technical_indicators_pb2_grpc import TechnicalIndicatorsServicer
from grpc_pbs.technical_indicators_pb2 import SMARequest, IndicatorBase, OneChannelIndicatorResponse, TradeAction, IndicatorGeneralInfo
from grpc_pbs.technical_indicators_pb2 import TRADE_ACTION_BUY, TRADE_ACTION_NONE, TRADE_ACTION_SELL, TRADE_ACTION_STRONG_BUY, TRADE_ACTION_STRONG_SELL
from google.protobuf.timestamp_pb2 import Timestamp

import numpy as np
import datetime


class IndiTestService(TechnicalIndicatorsServicer):

    def __init__(self):
        pass

    def GetSMA(self, request: SMARequest, context) -> OneChannelIndicatorResponse:
        symbol = request.base.symbol
        print(symbol)
        start_date: Timestamp = request.base.start_date
        end_date: Timestamp = request.base.end_date
        e1 = start_date.ToDatetime()
        e2 = end_date.ToDatetime()
        print(start_date)
        print(e1)
        print(end_date)
        print(e2)
        period = request.period
        values = np.random.randint(0, period, 50)
        t_v = TradeAction.values()
        t_a = TradeAction.keys()
        a = TRADE_ACTION_NONE
        e = TradeAction.Name(0)
        r_t_a = [TRADE_ACTION_NONE] * 50
        info = IndicatorGeneralInfo(success=True,
                                    error_msg="",
                                    start_date=start_date,
                                    end_date=end_date,
                                    recommended_trade_action=r_t_a)
        return OneChannelIndicatorResponse(info=info, values=values)
