# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: stock_financial_analytics.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1fstock_financial_analytics.proto\"\x9c\x01\n\x14StockAnalysisRequest\x12\x14\n\x0cstock_symbol\x18\x01 \x01(\t\x12\x17\n\nstart_year\x18\x02 \x01(\x05H\x00\x88\x01\x01\x12\x15\n\x08\x65nd_year\x18\x03 \x01(\x05H\x01\x88\x01\x01\x12\x15\n\x08language\x18\x04 \x01(\tH\x02\x88\x01\x01\x42\r\n\x0b_start_yearB\x0b\n\t_end_yearB\x0b\n\t_language\"\xad\x05\n\x15StockAnalysisResponse\x12\x0f\n\x07success\x18\x32 \x01(\x08\x12\x11\n\terror_msg\x18\x33 \x01(\t\x12\r\n\x05years\x18\x01 \x03(\x05\x12\x0f\n\x07revenue\x18\x02 \x03(\x02\x12\x1a\n\x12operating_expenses\x18\x04 \x03(\x02\x12\x12\n\nnet_income\x18\x05 \x03(\x02\x12\x18\n\x10operating_income\x18\x06 \x03(\x02\x12\x0e\n\x06\x65\x62itda\x18\x07 \x03(\x02\x12\x1a\n\x12\x64iluted_net_income\x18\x08 \x03(\x02\x12\x0e\n\x06\x61ssets\x18\t \x03(\x02\x12\x16\n\x0e\x63urrent_assets\x18\n \x03(\x02\x12\x13\n\x0binventories\x18\x0b \x03(\x02\x12\x1b\n\x13\x63urrent_liabilities\x18\x0c \x03(\x02\x12\x0c\n\x04\x64\x65\x62t\x18\r \x03(\x02\x12\x10\n\x08net_debt\x18\x0e \x03(\x02\x12\x1c\n\x14\x63\x61pital_expenditures\x18\x0f \x03(\x02\x12&\n\x1e\x63\x61sh_from_operating_activities\x18\x10 \x03(\x02\x12\x16\n\x0e\x66ree_cash_flow\x18\x11 \x03(\x02\x12\x0b\n\x03roa\x18\x12 \x03(\x02\x12\x0b\n\x03roe\x18\x13 \x03(\x02\x12\x18\n\x10operating_margin\x18\x14 \x03(\x02\x12\x12\n\nnet_margin\x18\x15 \x03(\x02\x12\x0b\n\x03\x64te\x18\x16 \x03(\x02\x12\x0b\n\x03\x64ta\x18\x17 \x03(\x02\x12\x15\n\rcurrent_ratio\x18\x18 \x03(\x02\x12\x13\n\x0bquick_ratio\x18\x19 \x03(\x02\x12\x0b\n\x03\x65ps\x18\x1a \x03(\x02\x12\n\n\x02pe\x18\x1b \x03(\x02\x12\n\n\x02ps\x18\x1c \x03(\x02\x12\x15\n\rdiv_per_share\x18\x1d \x03(\x02\x12\x11\n\tdiv_yield\x18\x1e \x03(\x02\x12\x12\n\ndiv_payout\x18\x1f \x03(\x02\x12\x11\n\tanalytics\x18  \x01(\t2X\n\x17StockFinancialAnalytics\x12=\n\x0cGetAnalytics\x12\x15.StockAnalysisRequest\x1a\x16.StockAnalysisResponseb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'stock_financial_analytics_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _STOCKANALYSISREQUEST._serialized_start=36
  _STOCKANALYSISREQUEST._serialized_end=192
  _STOCKANALYSISRESPONSE._serialized_start=195
  _STOCKANALYSISRESPONSE._serialized_end=880
  _STOCKFINANCIALANALYTICS._serialized_start=882
  _STOCKFINANCIALANALYTICS._serialized_end=970
# @@protoc_insertion_point(module_scope)
