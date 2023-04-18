from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor
TRADE_ACTION_BUY: TradeAction
TRADE_ACTION_NONE: TradeAction
TRADE_ACTION_SELL: TradeAction
TRADE_ACTION_STRONG_BUY: TradeAction
TRADE_ACTION_STRONG_SELL: TradeAction

class AlligatorRequest(_message.Message):
    __slots__ = ["base"]
    BASE_FIELD_NUMBER: _ClassVar[int]
    base: IndicatorBase
    def __init__(self, base: _Optional[_Union[IndicatorBase, _Mapping]] = ...) -> None: ...

class AlligatorResponse(_message.Message):
    __slots__ = ["info", "jaw", "lips", "teeth"]
    INFO_FIELD_NUMBER: _ClassVar[int]
    JAW_FIELD_NUMBER: _ClassVar[int]
    LIPS_FIELD_NUMBER: _ClassVar[int]
    TEETH_FIELD_NUMBER: _ClassVar[int]
    info: IndicatorGeneralInfo
    jaw: _containers.RepeatedScalarFieldContainer[float]
    lips: _containers.RepeatedScalarFieldContainer[float]
    teeth: _containers.RepeatedScalarFieldContainer[float]
    def __init__(self, info: _Optional[_Union[IndicatorGeneralInfo, _Mapping]] = ..., jaw: _Optional[_Iterable[float]] = ..., teeth: _Optional[_Iterable[float]] = ..., lips: _Optional[_Iterable[float]] = ...) -> None: ...

class BollingerBandsRequest(_message.Message):
    __slots__ = ["base", "ma_period", "width_factor"]
    BASE_FIELD_NUMBER: _ClassVar[int]
    MA_PERIOD_FIELD_NUMBER: _ClassVar[int]
    WIDTH_FACTOR_FIELD_NUMBER: _ClassVar[int]
    base: IndicatorBase
    ma_period: int
    width_factor: int
    def __init__(self, base: _Optional[_Union[IndicatorBase, _Mapping]] = ..., ma_period: _Optional[int] = ..., width_factor: _Optional[int] = ...) -> None: ...

class BollingerBandsResponse(_message.Message):
    __slots__ = ["info", "lower_band", "ma", "upper_band"]
    INFO_FIELD_NUMBER: _ClassVar[int]
    LOWER_BAND_FIELD_NUMBER: _ClassVar[int]
    MA_FIELD_NUMBER: _ClassVar[int]
    UPPER_BAND_FIELD_NUMBER: _ClassVar[int]
    info: IndicatorGeneralInfo
    lower_band: _containers.RepeatedScalarFieldContainer[float]
    ma: _containers.RepeatedScalarFieldContainer[float]
    upper_band: _containers.RepeatedScalarFieldContainer[float]
    def __init__(self, info: _Optional[_Union[IndicatorGeneralInfo, _Mapping]] = ..., lower_band: _Optional[_Iterable[float]] = ..., ma: _Optional[_Iterable[float]] = ..., upper_band: _Optional[_Iterable[float]] = ...) -> None: ...

class EMARequest(_message.Message):
    __slots__ = ["base", "period", "smoothing_factor"]
    BASE_FIELD_NUMBER: _ClassVar[int]
    PERIOD_FIELD_NUMBER: _ClassVar[int]
    SMOOTHING_FACTOR_FIELD_NUMBER: _ClassVar[int]
    base: IndicatorBase
    period: int
    smoothing_factor: float
    def __init__(self, base: _Optional[_Union[IndicatorBase, _Mapping]] = ..., period: _Optional[int] = ..., smoothing_factor: _Optional[float] = ...) -> None: ...

class IndicatorBase(_message.Message):
    __slots__ = ["end_date", "start_date", "symbol"]
    END_DATE_FIELD_NUMBER: _ClassVar[int]
    START_DATE_FIELD_NUMBER: _ClassVar[int]
    SYMBOL_FIELD_NUMBER: _ClassVar[int]
    end_date: _timestamp_pb2.Timestamp
    start_date: _timestamp_pb2.Timestamp
    symbol: str
    def __init__(self, symbol: _Optional[str] = ..., start_date: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., end_date: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class IndicatorGeneralInfo(_message.Message):
    __slots__ = ["dates", "error_msg", "recommended_trade_action", "success"]
    DATES_FIELD_NUMBER: _ClassVar[int]
    ERROR_MSG_FIELD_NUMBER: _ClassVar[int]
    RECOMMENDED_TRADE_ACTION_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    dates: _containers.RepeatedCompositeFieldContainer[_timestamp_pb2.Timestamp]
    error_msg: str
    recommended_trade_action: _containers.RepeatedScalarFieldContainer[TradeAction]
    success: bool
    def __init__(self, success: bool = ..., error_msg: _Optional[str] = ..., dates: _Optional[_Iterable[_Union[_timestamp_pb2.Timestamp, _Mapping]]] = ..., recommended_trade_action: _Optional[_Iterable[_Union[TradeAction, str]]] = ...) -> None: ...

class MACDRequest(_message.Message):
    __slots__ = ["base", "fast_period", "signal_period", "slow_period"]
    BASE_FIELD_NUMBER: _ClassVar[int]
    FAST_PERIOD_FIELD_NUMBER: _ClassVar[int]
    SIGNAL_PERIOD_FIELD_NUMBER: _ClassVar[int]
    SLOW_PERIOD_FIELD_NUMBER: _ClassVar[int]
    base: IndicatorBase
    fast_period: int
    signal_period: int
    slow_period: int
    def __init__(self, base: _Optional[_Union[IndicatorBase, _Mapping]] = ..., fast_period: _Optional[int] = ..., slow_period: _Optional[int] = ..., signal_period: _Optional[int] = ...) -> None: ...

class MACDResponse(_message.Message):
    __slots__ = ["diff", "info", "macd", "signal"]
    DIFF_FIELD_NUMBER: _ClassVar[int]
    INFO_FIELD_NUMBER: _ClassVar[int]
    MACD_FIELD_NUMBER: _ClassVar[int]
    SIGNAL_FIELD_NUMBER: _ClassVar[int]
    diff: _containers.RepeatedScalarFieldContainer[float]
    info: IndicatorGeneralInfo
    macd: _containers.RepeatedScalarFieldContainer[float]
    signal: _containers.RepeatedScalarFieldContainer[float]
    def __init__(self, info: _Optional[_Union[IndicatorGeneralInfo, _Mapping]] = ..., macd: _Optional[_Iterable[float]] = ..., signal: _Optional[_Iterable[float]] = ..., diff: _Optional[_Iterable[float]] = ...) -> None: ...

class OneChannelIndicatorResponse(_message.Message):
    __slots__ = ["info", "values"]
    INFO_FIELD_NUMBER: _ClassVar[int]
    VALUES_FIELD_NUMBER: _ClassVar[int]
    info: IndicatorGeneralInfo
    values: _containers.RepeatedScalarFieldContainer[float]
    def __init__(self, info: _Optional[_Union[IndicatorGeneralInfo, _Mapping]] = ..., values: _Optional[_Iterable[float]] = ...) -> None: ...

class RSIRequest(_message.Message):
    __slots__ = ["base", "period"]
    BASE_FIELD_NUMBER: _ClassVar[int]
    PERIOD_FIELD_NUMBER: _ClassVar[int]
    base: IndicatorBase
    period: int
    def __init__(self, base: _Optional[_Union[IndicatorBase, _Mapping]] = ..., period: _Optional[int] = ...) -> None: ...

class RVIRequest(_message.Message):
    __slots__ = ["base", "signal_period", "smoothing_period"]
    BASE_FIELD_NUMBER: _ClassVar[int]
    SIGNAL_PERIOD_FIELD_NUMBER: _ClassVar[int]
    SMOOTHING_PERIOD_FIELD_NUMBER: _ClassVar[int]
    base: IndicatorBase
    signal_period: int
    smoothing_period: int
    def __init__(self, base: _Optional[_Union[IndicatorBase, _Mapping]] = ..., smoothing_period: _Optional[int] = ..., signal_period: _Optional[int] = ...) -> None: ...

class RVIResponse(_message.Message):
    __slots__ = ["info", "rvi", "signal"]
    INFO_FIELD_NUMBER: _ClassVar[int]
    RVI_FIELD_NUMBER: _ClassVar[int]
    SIGNAL_FIELD_NUMBER: _ClassVar[int]
    info: IndicatorGeneralInfo
    rvi: _containers.RepeatedScalarFieldContainer[float]
    signal: _containers.RepeatedScalarFieldContainer[float]
    def __init__(self, info: _Optional[_Union[IndicatorGeneralInfo, _Mapping]] = ..., rvi: _Optional[_Iterable[float]] = ..., signal: _Optional[_Iterable[float]] = ...) -> None: ...

class RoCRequest(_message.Message):
    __slots__ = ["base", "period"]
    BASE_FIELD_NUMBER: _ClassVar[int]
    PERIOD_FIELD_NUMBER: _ClassVar[int]
    base: IndicatorBase
    period: int
    def __init__(self, base: _Optional[_Union[IndicatorBase, _Mapping]] = ..., period: _Optional[int] = ...) -> None: ...

class SMARequest(_message.Message):
    __slots__ = ["base", "period"]
    BASE_FIELD_NUMBER: _ClassVar[int]
    PERIOD_FIELD_NUMBER: _ClassVar[int]
    base: IndicatorBase
    period: int
    def __init__(self, base: _Optional[_Union[IndicatorBase, _Mapping]] = ..., period: _Optional[int] = ...) -> None: ...

class WMARequest(_message.Message):
    __slots__ = ["base", "period"]
    BASE_FIELD_NUMBER: _ClassVar[int]
    PERIOD_FIELD_NUMBER: _ClassVar[int]
    base: IndicatorBase
    period: int
    def __init__(self, base: _Optional[_Union[IndicatorBase, _Mapping]] = ..., period: _Optional[int] = ...) -> None: ...

class TradeAction(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
