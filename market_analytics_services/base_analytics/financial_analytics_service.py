from datetime import datetime

from grpc_pbs.stock_financial_analytics_pb2 import StockAnalysisRequest, StockAnalysisResponse
from grpc_pbs.stock_financial_analytics_pb2_grpc import StockFinancialAnalyticsServicer

import psycopg2

from market_analytics_services.base_analytics.ai_expert_agent import AIExpertAgent
from market_analytics_services.base_analytics.data_manager import DataManager


class StockFinancialAnalyticsService(StockFinancialAnalyticsServicer):
    def __init__(self, conn: psycopg2._psycopg.connection):
        self.data_manager = DataManager(conn)
        #self.ai_expert_agent = AIExpertAgent()

    def GetAnalytics(self, request: StockAnalysisRequest, context) -> StockAnalysisResponse:
        try:
            metrics = self.data_manager.load_data(request)
            years, metrcis_str = self.data_manager.get_data_string(metrics_df=metrics, request=request)
            lang = "RUS" if (request.language not in ["RUS", "ENG"]) else request.language
            #analytics = self.ai_expert_agent.ask_for_analysis(request.stock_symbol, metrcis_str, lang)
            ai_expert_agent = AIExpertAgent()
            analytics = ai_expert_agent.ask_for_analysis(request.stock_symbol, years, metrcis_str, lang)
            if request.stock_symbol.upper() == "НОВАТЭК":
                return StockAnalysisResponse(success=True, error_msg="",
                                             years=metrics["date"].to_list(),
                                             revenue=metrics["Revenue"].to_list(),
                                             operating_income=metrics["Operating Income"].to_list(),
                                             ebitda=metrics["EBITDA"].to_list(),
                                             diluted_net_income=metrics["Diluted Net Income"].to_list(),
                                             cash_from_operating_activities=metrics["Cash From Operating Activities"].to_list(),
                                             capital_expenditures=metrics["Capital Expenditures"].to_list(),
                                             free_cash_flow=metrics["Free Cash Flow"].to_list(),
                                             analytics=analytics)
            else:
                return StockAnalysisResponse(success=True, error_msg="",
                                             years=metrics["date"].to_list(),
                                             revenue=metrics["Revenue"].to_list(),
                                             operating_expenses=metrics["Operating Expenses"].to_list(),
                                             operating_income=metrics["Operating Income"].to_list(),
                                             ebitda=metrics["EBITDA"].to_list(),
                                             net_income=metrics["Net Income"].to_list(),
                                             diluted_net_income=metrics["Diluted Net Income"].to_list(),
                                             assets=metrics["Total Assets"].to_list(),
                                             current_assets=metrics["Current Assets"].to_list(),
                                             inventories=metrics["Inventories"].to_list(),
                                             current_liabilities=metrics["Total Current Liabilities"].to_list(),
                                             debt=metrics["Total Debt"].to_list(),
                                             net_debt=metrics["Net Debt"].to_list(),
                                             cash_from_operating_activities=metrics[
                                                 "Cash From Operating Activities"].to_list(),
                                             capital_expenditures=metrics["Capital Expenditures"].to_list(),
                                             free_cash_flow=metrics["Free Cash Flow"].to_list(),
                                             roa=metrics["ROA"].to_list(),
                                             roe=metrics["ROE"].to_list(),
                                             operating_margin=metrics["Operating margin"].to_list(),
                                             net_margin=metrics["Net margin"].to_list(),
                                             dta=metrics["Debt to assets ratio"].to_list(),
                                             dte=metrics["Debt to equity ratio"].to_list(),
                                             current_ratio=metrics["Current ratio"].to_list(),
                                             quick_ratio=metrics["Quick ratio"].to_list(),
                                             pe=metrics["PE"].to_list(),
                                             ps=metrics["PS"].to_list(),
                                             eps=metrics["EPS"].to_list(),
                                             div_per_share=metrics["Dividends per share"].to_list(),
                                             div_yield=metrics["Dividend yield"].to_list(),
                                             div_payout=metrics["Dividend payout"].to_list(),
                                             analytics=analytics)
        except Exception as e:
            return StockAnalysisResponse(success=False, error_msg=e.__str__())

    def _test(self, r: StockAnalysisRequest):
        years, dd = self.data_manager.get_data_string(r)
        lang = "RUS" if (r.language not in ["RUS", "ENG"]) else r.language
        ms = AIExpertAgent().ask_for_analysis(r.stock_symbol, years, dd, lang)
        print(ms)


if __name__ == "__main__":
    conn = psycopg2.connect(dbname='politehdb',
                            user='politeh',
                            password='RxKWF20V6f0K',
                            host='188.120.230.134',
                            port='5432')
    s = StockFinancialAnalyticsService(conn)
    start_date = datetime(year=2000, month=1, day=1)
    end_date = datetime(year=2020, month=1, day=1)
    # start_date_t = Timestamp()
    # end_date_t = Timestamp()
    # start_date_t.FromDatetime(start_date)
    # end_date_t.FromDatetime(end_date)
    #r = StockAnalysisRequest(stock_symbol="газпром", start_date=start_date_t, end_date=end_date_t)
    r = StockAnalysisRequest(stock_symbol="новатэк")
    s._test(r)


