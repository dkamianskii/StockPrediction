# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from grpc_pbs import stock_financial_analytics_pb2 as stock__financial__analytics__pb2


class StockFinancialAnalyticsStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.GetAnalytics = channel.unary_unary(
                '/StockFinancialAnalytics/GetAnalytics',
                request_serializer=stock__financial__analytics__pb2.StockAnalysisRequest.SerializeToString,
                response_deserializer=stock__financial__analytics__pb2.StockAnalysisResponse.FromString,
                )


class StockFinancialAnalyticsServicer(object):
    """Missing associated documentation comment in .proto file."""

    def GetAnalytics(self, request, context):
        """When a new financial data comes it requires a processing to calculate and save to db all needed metrics
        rpc ProcessDataDump(StockDataDumpRequest) returns (StockDataDumpResponse);

        This method is called to receive analytics info about stock
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_StockFinancialAnalyticsServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'GetAnalytics': grpc.unary_unary_rpc_method_handler(
                    servicer.GetAnalytics,
                    request_deserializer=stock__financial__analytics__pb2.StockAnalysisRequest.FromString,
                    response_serializer=stock__financial__analytics__pb2.StockAnalysisResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'StockFinancialAnalytics', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class StockFinancialAnalytics(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def GetAnalytics(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/StockFinancialAnalytics/GetAnalytics',
            stock__financial__analytics__pb2.StockAnalysisRequest.SerializeToString,
            stock__financial__analytics__pb2.StockAnalysisResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)