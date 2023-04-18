# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: technical_indicators.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1atechnical_indicators.proto\x1a\x1fgoogle/protobuf/timestamp.proto\"\xa3\x01\n\rIndicatorBase\x12\x0e\n\x06symbol\x18\x01 \x01(\t\x12\x33\n\nstart_date\x18\x02 \x01(\x0b\x32\x1a.google.protobuf.TimestampH\x00\x88\x01\x01\x12\x31\n\x08\x65nd_date\x18\x03 \x01(\x0b\x32\x1a.google.protobuf.TimestampH\x01\x88\x01\x01\x42\r\n\x0b_start_dateB\x0b\n\t_end_date\"\x95\x01\n\x14IndicatorGeneralInfo\x12\x0f\n\x07success\x18\x01 \x01(\x08\x12\x11\n\terror_msg\x18\x02 \x01(\t\x12)\n\x05\x64\x61tes\x18\x03 \x03(\x0b\x32\x1a.google.protobuf.Timestamp\x12.\n\x18recommended_trade_action\x18\x04 \x03(\x0e\x32\x0c.TradeAction\"R\n\x1bOneChannelIndicatorResponse\x12#\n\x04info\x18\x01 \x01(\x0b\x32\x15.IndicatorGeneralInfo\x12\x0e\n\x06values\x18\x02 \x03(\x02\":\n\nSMARequest\x12\x1c\n\x04\x62\x61se\x18\x01 \x01(\x0b\x32\x0e.IndicatorBase\x12\x0e\n\x06period\x18\x02 \x01(\r\"n\n\nEMARequest\x12\x1c\n\x04\x62\x61se\x18\x01 \x01(\x0b\x32\x0e.IndicatorBase\x12\x0e\n\x06period\x18\x02 \x01(\r\x12\x1d\n\x10smoothing_factor\x18\x03 \x01(\x02H\x00\x88\x01\x01\x42\x13\n\x11_smoothing_factor\":\n\nWMARequest\x12\x1c\n\x04\x62\x61se\x18\x01 \x01(\x0b\x32\x0e.IndicatorBase\x12\x0e\n\x06period\x18\x02 \x01(\r\":\n\nRoCRequest\x12\x1c\n\x04\x62\x61se\x18\x01 \x01(\x0b\x32\x0e.IndicatorBase\x12\x0e\n\x06period\x18\x02 \x01(\r\"\xad\x01\n\x0bMACDRequest\x12\x1c\n\x04\x62\x61se\x18\x01 \x01(\x0b\x32\x0e.IndicatorBase\x12\x18\n\x0b\x66\x61st_period\x18\x02 \x01(\rH\x00\x88\x01\x01\x12\x18\n\x0bslow_period\x18\x03 \x01(\rH\x01\x88\x01\x01\x12\x1a\n\rsignal_period\x18\x04 \x01(\rH\x02\x88\x01\x01\x42\x0e\n\x0c_fast_periodB\x0e\n\x0c_slow_periodB\x10\n\x0e_signal_period\"_\n\x0cMACDResponse\x12#\n\x04info\x18\x01 \x01(\x0b\x32\x15.IndicatorGeneralInfo\x12\x0c\n\x04macd\x18\x02 \x03(\x02\x12\x0e\n\x06signal\x18\x03 \x03(\x02\x12\x0c\n\x04\x64iff\x18\x04 \x03(\x02\":\n\nRSIRequest\x12\x1c\n\x04\x62\x61se\x18\x01 \x01(\x0b\x32\x0e.IndicatorBase\x12\x0e\n\x06period\x18\x02 \x01(\r\"0\n\x10\x41lligatorRequest\x12\x1c\n\x04\x62\x61se\x18\x01 \x01(\x0b\x32\x0e.IndicatorBase\"b\n\x11\x41lligatorResponse\x12#\n\x04info\x18\x01 \x01(\x0b\x32\x15.IndicatorGeneralInfo\x12\x0b\n\x03jaw\x18\x02 \x03(\x02\x12\r\n\x05teeth\x18\x03 \x03(\x02\x12\x0c\n\x04lips\x18\x04 \x03(\x02\"\x87\x01\n\x15\x42ollingerBandsRequest\x12\x1c\n\x04\x62\x61se\x18\x01 \x01(\x0b\x32\x0e.IndicatorBase\x12\x16\n\tma_period\x18\x02 \x01(\rH\x00\x88\x01\x01\x12\x19\n\x0cwidth_factor\x18\x03 \x01(\rH\x01\x88\x01\x01\x42\x0c\n\n_ma_periodB\x0f\n\r_width_factor\"q\n\x16\x42ollingerBandsResponse\x12#\n\x04info\x18\x01 \x01(\x0b\x32\x15.IndicatorGeneralInfo\x12\x12\n\nlower_band\x18\x02 \x03(\x02\x12\n\n\x02ma\x18\x03 \x03(\x02\x12\x12\n\nupper_band\x18\x04 \x03(\x02\"\x8c\x01\n\nRVIRequest\x12\x1c\n\x04\x62\x61se\x18\x01 \x01(\x0b\x32\x0e.IndicatorBase\x12\x1d\n\x10smoothing_period\x18\x03 \x01(\rH\x00\x88\x01\x01\x12\x1a\n\rsignal_period\x18\x04 \x01(\rH\x01\x88\x01\x01\x42\x13\n\x11_smoothing_periodB\x10\n\x0e_signal_period\"O\n\x0bRVIResponse\x12#\n\x04info\x18\x01 \x01(\x0b\x32\x15.IndicatorGeneralInfo\x12\x0b\n\x03rvi\x18\x02 \x03(\x02\x12\x0e\n\x06signal\x18\x03 \x03(\x02*\x8c\x01\n\x0bTradeAction\x12\x15\n\x11TRADE_ACTION_NONE\x10\x00\x12\x14\n\x10TRADE_ACTION_BUY\x10\x01\x12\x1b\n\x17TRADE_ACTION_STRONG_BUY\x10\x02\x12\x15\n\x11TRADE_ACTION_SELL\x10\x03\x12\x1c\n\x18TRADE_ACTION_STRONG_SELL\x10\x04\x32\xe8\x03\n\x13TechnicalIndicators\x12\x33\n\x06GetSMA\x12\x0b.SMARequest\x1a\x1c.OneChannelIndicatorResponse\x12\x33\n\x06GetEMA\x12\x0b.EMARequest\x1a\x1c.OneChannelIndicatorResponse\x12\x33\n\x06GetWMA\x12\x0b.WMARequest\x1a\x1c.OneChannelIndicatorResponse\x12\x33\n\x06GetRoC\x12\x0b.RoCRequest\x1a\x1c.OneChannelIndicatorResponse\x12&\n\x07GetMACD\x12\x0c.MACDRequest\x1a\r.MACDResponse\x12\x33\n\x06GetRSI\x12\x0b.RSIRequest\x1a\x1c.OneChannelIndicatorResponse\x12\x35\n\x0cGetAlligator\x12\x11.AlligatorRequest\x1a\x12.AlligatorResponse\x12\x44\n\x11GetBollingerBands\x12\x16.BollingerBandsRequest\x1a\x17.BollingerBandsResponse\x12#\n\x06GetRVI\x12\x0b.RVIRequest\x1a\x0c.RVIResponseb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'technical_indicators_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _TRADEACTION._serialized_start=1718
  _TRADEACTION._serialized_end=1858
  _INDICATORBASE._serialized_start=64
  _INDICATORBASE._serialized_end=227
  _INDICATORGENERALINFO._serialized_start=230
  _INDICATORGENERALINFO._serialized_end=379
  _ONECHANNELINDICATORRESPONSE._serialized_start=381
  _ONECHANNELINDICATORRESPONSE._serialized_end=463
  _SMAREQUEST._serialized_start=465
  _SMAREQUEST._serialized_end=523
  _EMAREQUEST._serialized_start=525
  _EMAREQUEST._serialized_end=635
  _WMAREQUEST._serialized_start=637
  _WMAREQUEST._serialized_end=695
  _ROCREQUEST._serialized_start=697
  _ROCREQUEST._serialized_end=755
  _MACDREQUEST._serialized_start=758
  _MACDREQUEST._serialized_end=931
  _MACDRESPONSE._serialized_start=933
  _MACDRESPONSE._serialized_end=1028
  _RSIREQUEST._serialized_start=1030
  _RSIREQUEST._serialized_end=1088
  _ALLIGATORREQUEST._serialized_start=1090
  _ALLIGATORREQUEST._serialized_end=1138
  _ALLIGATORRESPONSE._serialized_start=1140
  _ALLIGATORRESPONSE._serialized_end=1238
  _BOLLINGERBANDSREQUEST._serialized_start=1241
  _BOLLINGERBANDSREQUEST._serialized_end=1376
  _BOLLINGERBANDSRESPONSE._serialized_start=1378
  _BOLLINGERBANDSRESPONSE._serialized_end=1491
  _RVIREQUEST._serialized_start=1494
  _RVIREQUEST._serialized_end=1634
  _RVIRESPONSE._serialized_start=1636
  _RVIRESPONSE._serialized_end=1715
  _TECHNICALINDICATORS._serialized_start=1861
  _TECHNICALINDICATORS._serialized_end=2349
# @@protoc_insertion_point(module_scope)