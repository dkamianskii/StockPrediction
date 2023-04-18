from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class StockAnalysisRequest(_message.Message):
    __slots__ = ["end_date", "language", "start_date", "stock_symbol"]
    END_DATE_FIELD_NUMBER: _ClassVar[int]
    LANGUAGE_FIELD_NUMBER: _ClassVar[int]
    START_DATE_FIELD_NUMBER: _ClassVar[int]
    STOCK_SYMBOL_FIELD_NUMBER: _ClassVar[int]
    end_date: _timestamp_pb2.Timestamp
    language: str
    start_date: _timestamp_pb2.Timestamp
    stock_symbol: str
    def __init__(self, stock_symbol: _Optional[str] = ..., start_date: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., end_date: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., language: _Optional[str] = ...) -> None: ...

class StockAnalysisResponse(_message.Message):
    __slots__ = ["analytics", "assets", "capital_expenditures", "cash_from_operating_activities", "current_assets", "current_liabilities", "current_ratio", "dates", "debt", "diluted_net_income", "div_payout", "div_per_share", "div_yield", "dta", "dte", "ebitda", "eps", "error_msg", "free_cash_flow", "inventories", "net_debt", "net_income", "net_margin", "operating_expenses", "operating_income", "operating_margin", "pe", "ps", "quick_ratio", "revenue", "roa", "roe", "success"]
    ANALYTICS_FIELD_NUMBER: _ClassVar[int]
    ASSETS_FIELD_NUMBER: _ClassVar[int]
    CAPITAL_EXPENDITURES_FIELD_NUMBER: _ClassVar[int]
    CASH_FROM_OPERATING_ACTIVITIES_FIELD_NUMBER: _ClassVar[int]
    CURRENT_ASSETS_FIELD_NUMBER: _ClassVar[int]
    CURRENT_LIABILITIES_FIELD_NUMBER: _ClassVar[int]
    CURRENT_RATIO_FIELD_NUMBER: _ClassVar[int]
    DATES_FIELD_NUMBER: _ClassVar[int]
    DEBT_FIELD_NUMBER: _ClassVar[int]
    DILUTED_NET_INCOME_FIELD_NUMBER: _ClassVar[int]
    DIV_PAYOUT_FIELD_NUMBER: _ClassVar[int]
    DIV_PER_SHARE_FIELD_NUMBER: _ClassVar[int]
    DIV_YIELD_FIELD_NUMBER: _ClassVar[int]
    DTA_FIELD_NUMBER: _ClassVar[int]
    DTE_FIELD_NUMBER: _ClassVar[int]
    EBITDA_FIELD_NUMBER: _ClassVar[int]
    EPS_FIELD_NUMBER: _ClassVar[int]
    ERROR_MSG_FIELD_NUMBER: _ClassVar[int]
    FREE_CASH_FLOW_FIELD_NUMBER: _ClassVar[int]
    INVENTORIES_FIELD_NUMBER: _ClassVar[int]
    NET_DEBT_FIELD_NUMBER: _ClassVar[int]
    NET_INCOME_FIELD_NUMBER: _ClassVar[int]
    NET_MARGIN_FIELD_NUMBER: _ClassVar[int]
    OPERATING_EXPENSES_FIELD_NUMBER: _ClassVar[int]
    OPERATING_INCOME_FIELD_NUMBER: _ClassVar[int]
    OPERATING_MARGIN_FIELD_NUMBER: _ClassVar[int]
    PE_FIELD_NUMBER: _ClassVar[int]
    PS_FIELD_NUMBER: _ClassVar[int]
    QUICK_RATIO_FIELD_NUMBER: _ClassVar[int]
    REVENUE_FIELD_NUMBER: _ClassVar[int]
    ROA_FIELD_NUMBER: _ClassVar[int]
    ROE_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    analytics: str
    assets: _containers.RepeatedScalarFieldContainer[float]
    capital_expenditures: _containers.RepeatedScalarFieldContainer[float]
    cash_from_operating_activities: _containers.RepeatedScalarFieldContainer[float]
    current_assets: _containers.RepeatedScalarFieldContainer[float]
    current_liabilities: _containers.RepeatedScalarFieldContainer[float]
    current_ratio: _containers.RepeatedScalarFieldContainer[float]
    dates: _containers.RepeatedCompositeFieldContainer[_timestamp_pb2.Timestamp]
    debt: _containers.RepeatedScalarFieldContainer[float]
    diluted_net_income: _containers.RepeatedScalarFieldContainer[float]
    div_payout: _containers.RepeatedScalarFieldContainer[float]
    div_per_share: _containers.RepeatedScalarFieldContainer[float]
    div_yield: _containers.RepeatedScalarFieldContainer[float]
    dta: _containers.RepeatedScalarFieldContainer[float]
    dte: _containers.RepeatedScalarFieldContainer[float]
    ebitda: _containers.RepeatedScalarFieldContainer[float]
    eps: _containers.RepeatedScalarFieldContainer[float]
    error_msg: str
    free_cash_flow: _containers.RepeatedScalarFieldContainer[float]
    inventories: _containers.RepeatedScalarFieldContainer[float]
    net_debt: _containers.RepeatedScalarFieldContainer[float]
    net_income: _containers.RepeatedScalarFieldContainer[float]
    net_margin: _containers.RepeatedScalarFieldContainer[float]
    operating_expenses: _containers.RepeatedScalarFieldContainer[float]
    operating_income: _containers.RepeatedScalarFieldContainer[float]
    operating_margin: _containers.RepeatedScalarFieldContainer[float]
    pe: _containers.RepeatedScalarFieldContainer[float]
    ps: _containers.RepeatedScalarFieldContainer[float]
    quick_ratio: _containers.RepeatedScalarFieldContainer[float]
    revenue: _containers.RepeatedScalarFieldContainer[float]
    roa: _containers.RepeatedScalarFieldContainer[float]
    roe: _containers.RepeatedScalarFieldContainer[float]
    success: bool
    def __init__(self, success: bool = ..., error_msg: _Optional[str] = ..., dates: _Optional[_Iterable[_Union[_timestamp_pb2.Timestamp, _Mapping]]] = ..., revenue: _Optional[_Iterable[float]] = ..., operating_expenses: _Optional[_Iterable[float]] = ..., net_income: _Optional[_Iterable[float]] = ..., operating_income: _Optional[_Iterable[float]] = ..., ebitda: _Optional[_Iterable[float]] = ..., diluted_net_income: _Optional[_Iterable[float]] = ..., assets: _Optional[_Iterable[float]] = ..., current_assets: _Optional[_Iterable[float]] = ..., inventories: _Optional[_Iterable[float]] = ..., current_liabilities: _Optional[_Iterable[float]] = ..., debt: _Optional[_Iterable[float]] = ..., net_debt: _Optional[_Iterable[float]] = ..., capital_expenditures: _Optional[_Iterable[float]] = ..., cash_from_operating_activities: _Optional[_Iterable[float]] = ..., free_cash_flow: _Optional[_Iterable[float]] = ..., roa: _Optional[_Iterable[float]] = ..., roe: _Optional[_Iterable[float]] = ..., operating_margin: _Optional[_Iterable[float]] = ..., net_margin: _Optional[_Iterable[float]] = ..., dte: _Optional[_Iterable[float]] = ..., dta: _Optional[_Iterable[float]] = ..., current_ratio: _Optional[_Iterable[float]] = ..., quick_ratio: _Optional[_Iterable[float]] = ..., eps: _Optional[_Iterable[float]] = ..., pe: _Optional[_Iterable[float]] = ..., ps: _Optional[_Iterable[float]] = ..., div_per_share: _Optional[_Iterable[float]] = ..., div_yield: _Optional[_Iterable[float]] = ..., div_payout: _Optional[_Iterable[float]] = ..., analytics: _Optional[str] = ...) -> None: ...
