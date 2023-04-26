from typing import Optional, Dict, Tuple

import numpy as np
import pandas as pd
import psycopg2

from grpc_pbs.stock_financial_analytics_pb2 import StockAnalysisRequest
import datetime

class DataManager:

    def __init__(self, conn: psycopg2._psycopg.connection):
        self.conn = conn
        self.min_max_date_available: Dict[str, Tuple] = {}
        with self.conn.cursor() as cursor:
            cursor.execute(f"""SELECT MIN(date), MAX(date) FROM novatek_fin_data""")
            min_max = cursor.fetchall()[0]
            self.min_max_date_available["НОВАТЭК"] = min_max
            cursor.execute(f"""SELECT MIN(year), MAX(year) FROM gazprom_financial_data""")
            min_max = cursor.fetchall()[0]
            self.min_max_date_available["ГАЗПРОМ"] = min_max

    def get_data_string(self, request: StockAnalysisRequest, metrics_df: Optional[pd.DataFrame] = None) -> str:
        if metrics_df is None:
            metrics_df = self.load_data(request)
        symbol = request.stock_symbol
        symbol = symbol.upper()
        if metrics_df.shape[0] > 3:
            metrics_df = metrics_df[-3:]
        if symbol == "НОВАТЭК":
            return f"""Revenue: {metrics_df['Revenue'].to_list()},Operating Income: {metrics_df['Operating Income'].to_list()},EBITDA: {metrics_df['EBITDA'].to_list()},Cash From Operating Activities: {metrics_df['Cash From Operating Activities'].to_list()},Capital Expenditures: {metrics_df['Capital Expenditures'].to_list()},Free Cash Flow: {metrics_df['Free Cash Flow'].to_list()}, EPS: {metrics_df['EPS'].to_list()}, for years: {metrics_df.index.to_list()} correspondingly"""
        elif symbol == "ГАЗПРОМ":
            data_string = f"Revenue: {metrics_df['Revenue'].to_list()},"
            data_string += f",Operating Expenses: {metrics_df['Operating Expenses'].to_list()}"
            data_string += f",Operating Income: {metrics_df['Operating Income'].to_list()}"
            data_string += f",EBITDA: {metrics_df['EBITDA'].to_list()}"
            data_string += f",Current Assets: {metrics_df['Current Assets'].to_list()}"
            data_string += f",Capital Expenditures: {metrics_df['Capital Expenditures'].to_list()}"
            data_string += f",RoA: {metrics_df['ROA'].to_list()}"
            data_string += f",Net margin: {metrics_df['Net margin'].to_list()}"
            data_string += f",Debt to assets ratio: {metrics_df['Debt to assets ratio'].to_list()}"
            data_string += f",PE: {metrics_df['PE'].to_list()}"
            data_string += f",EPS: {metrics_df['EPS'].to_list()}"
            data_string += f",Dividend yield: {metrics_df['Dividend yield'].to_list()}"
            data_string += f" for years: {metrics_df.index.to_list()} correspondingly"
            return data_string
        else:
            raise ValueError("Unknown stock symbol was passed")

    def load_data(self, request: StockAnalysisRequest) -> pd.DataFrame:
        symbol = request.stock_symbol
        symbol = symbol.upper()
        start_date = request.start_year
        end_date = request.end_year
        if not request.HasField('start_year') or start_date < self.min_max_date_available[symbol][0]:
            start_date = self.min_max_date_available[symbol][0]
        if not request.HasField('end_year') or end_date > self.min_max_date_available[symbol][1]:
            end_date = self.min_max_date_available[symbol][1]
        if symbol == "НОВАТЭК":
            with self.conn.cursor() as cursor:
                date_bounds = f" AND date >= {start_date} AND date <= {end_date}"
                cursor.execute(f"""SELECT DISTINCT date FROM novatek_fin_data
                                                 WHERE{date_bounds[4:]}
                                                 ORDER BY date ASC""")
                df = pd.DataFrame(cursor.fetchall(), columns=["date"])
                metrics = [('Revenue','Выручка от реализации '), ('Operating Income','Операционная прибыль нормализованная'),
                           ('EBITDA','EBITDA нормализованная, включая долю в EBITDA совместных предприятий'),
                           ('Diluted Net Income','Прибыль, относящаяся к акционерам ПАО «НОВАТЭК», нормализованная(4) без учета эффекта от курсовых разниц'),
                           ('Cash From Operating Activities','Операционный денежный поток'),
                           ('Capital Expenditures','Денежные средства, использованные на оплату капитальных вложений'),
                           ('Free Cash Flow','Свободный денежный поток')]
                for metric in metrics:
                    cursor.execute(f"""SELECT current_year_indexes  FROM novatek_fin_data
                                                                     WHERE financial_indexes = '{metric[1]}'{date_bounds}
                                                                     ORDER BY date ASC""")
                    vals = cursor.fetchall()
                    df[metric[0]] = [val[0] for val in vals]
                    if metric[0] == 'Capital Expenditures':
                        df[metric[0]] *= -1
                cursor.execute(f"""SELECT current_year_indexes  FROM novatek_fin_data
                                   WHERE (financial_indexes = 'Прибыль, относящаяся к акционерам ПАО «НОВАТЭК», нормализованная(4) без учета эффекта от курсовых разниц' OR 
                                   financial_indexes = 'Прибыль, относящаяся к акционерам ПАО «НОВАТЭК», нормализованная' OR
                                   financial_indexes = 'Прибыль, относящаяся к акционерам ОАО «НОВАТЭК»'){date_bounds}
                                   ORDER BY date ASC""")
                vals = cursor.fetchall()
                df["EPS"] = [val[0] for val in vals]
        elif symbol == "ГАЗПРОМ":
            with self.conn.cursor() as cursor:
                date_bounds = f" AND year >= {start_date} AND year <= {end_date}"
                cursor.execute(f"""SELECT DISTINCT year FROM gazprom_financial_data
                                                            WHERE{date_bounds[4:]}
                                                            ORDER BY year ASC""")
                df = pd.DataFrame(cursor.fetchall(), columns=["date"])
                metrics = [('Revenue', 'Выручка от продаж, млн руб.'),
                           ('Operating Expenses','Операционные расходы, млн руб.'),
                           ('Operating Income', 'Прибыль от продаж, млн руб.'),
                           ('EBITDA', 'Приведенный показатель EBITDA, млн руб.'),
                           ('Net Income','Прибыль за год, млн руб.'),
                           ('Diluted Net Income',"""Прибыль за год, относящаяся к акционерам
ПАО «Газпром», млн руб."""),
                           ('Total Assets','Активы, млн руб.'),
                           ('Current Assets', 'Оборотные активы, млн руб.'),
                           ('Inventories','Товарно-материальные запасы, млн руб.'),
                           ('Total Current Liabilities','Краткосрочные обязательства, млн руб.'),
                           ('Total Debt', 'Общий долг, млн руб.'),
                           ('Net Debt', 'Чистый долг, млн руб.'),
                           ('Cash From Operating Activities', 'Чистые денежные средства от операционной деятельности, млн руб.'),
                           ('Capital Expenditures', 'Капитальные вложения, млн руб.'),
                           ('Free Cash Flow', 'Денежные средства и их эквиваленты на конец отчетного года, млн руб.'),
                           ('ROA','Рентабельность активов (ROA)'),
                           ('ROE',"""Рентабельность акционерного (собственного) 
капитала (ROE)"""),
                           ('Operating margin','Рентабельность прибыли от продаж (операционная рентабельность)'),
                           ('Net margin', 'Рентабельность прибыли за год'),
                           ('Debt to equity ratio', 'Отношение общего долга к сумме общего долга, акционерного капитала и неконтролирующей доле участия'),
                           ('Debt to assets ratio', 'Отношение общего долга к общим активам'),
                           ('Current ratio', 'Коэффициент текущей ликвидности'),
                           ('Quick ratio', 'Коэффициент быстрой ликвидности'),
                           ('PE','Коэффициент P / E'),
                           ('PS','Коэффициент P / S'),
                           ('EPS', """Базовая и разводненная прибыль в расчете на одну акцию, относящаяся к акционерам ПАО «Газпром» 
(в российских рублях), руб.""")]
                for metric in metrics:
                    if metric[0] == 'Capital Expenditures':
                        cursor.execute(f"""SELECT MIN(amount_rub) FROM gazprom_financial_data
                                                                            WHERE name = '{metric[1]}'{date_bounds}
                                                                            GROUP BY year
                                                                            ORDER BY year ASC""")
                    else:
                        cursor.execute(f"""SELECT amount_rub FROM gazprom_financial_data
                                                                            WHERE name = '{metric[1]}'{date_bounds}
                                                                                    ORDER BY year ASC""")
                    vals = cursor.fetchall()
                    df[metric[0]] = [val[0] for val in vals]
                cursor.execute(f"""SELECT amount FROM
                                                     gazprom_indicators_data
                                                     WHERE name = 'Количество выпущенных обыкновенных акций ПАО «Газпром» по состоянию на конец года'{date_bounds}
                                                     ORDER BY year ASC""")
                shares = np.array([val[0] for val in cursor.fetchall()])
                cursor.execute(f"""SELECT amount FROM
                                                     gazprom_indicators_data
                                                     WHERE name = 'Дивиденды на обыкновенную акцию'{date_bounds}
                                                     ORDER BY year ASC""")
                divs_per_share = np.array([val[0] for val in cursor.fetchall()])
                cursor.execute(f"""SELECT amount FROM
                                                     gazprom_indicators_data
                                                     WHERE name = 'Цена за акцию на закрытие торгов на ПАО Московская Биржа, на конец года'{date_bounds}
                                                     ORDER BY year ASC""")
                price = np.array([val[0] for val in cursor.fetchall()])
                df["Dividends per share"] = divs_per_share
                df["Dividend yield"] = divs_per_share / price
                df["Dividend payout"] = divs_per_share * shares / df["Net Income"].to_numpy()
        else:
            raise ValueError("Unknown stock symbol was passed")
        df.index = df["date"]
        return df