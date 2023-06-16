import numpy as np
import yfinance as yf
import pandas as pd
from tvDatafeed import TvDatafeed, Interval
from prediction_models.config import RAW_STOCKS, STOCKS_DIFF, tvdatafeed_user, tvdatafeed_password

sp500_tickers = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')[0]['Symbol'].tolist()
hk35_tickers = ['1', '2', '3', '5', '6', '8', '11', '12', '16', '17', '19', '27', '66', '101', '288', '267', '293',
                '316', '388', '522', '669', '823', '853', '1038', '1113', '1299', '1308', '1928', '1972', '1997',
                '2269', '2388', '2888', '6969'] #.HK
imoex_tickers = ['AFKS', 'AFLT', 'ALRS', 'AGRO', 'CHMF', 'ENPG', 'FIVE', 'FIXP', 'GLTR',
                 'GAZP', 'GMKN',
                 'HYDR', 'IRAO', 'LKOH', 'MAGN', 'MGNT', 'MTSS', 'NLMK', 'NVTK', 'OZON',
                 'PHOR', 'ROSN',
                 'RTKM', 'PLZL', 'POLY', 'RUAL', 'TCSG', 'VKCO', 'YNDX', 'SBER', 'SNGS',
                 'TATN', 'TRNFP', 'VTBR'] #.ME
ftse_100_tickers = pd.read_html('https://en.wikipedia.org/wiki/FTSE_100_Index#Constituents')[4]['Ticker'].tolist() # .L


if __name__ == "__main__":
    # for name in sp500_tickers:
    #     print(name)
    #     t = yf.Ticker(name)
    #     df = t.history(start='2000-01-01', end='2023-01-01')
    #     if df.shape[0] == 0:
    #         continue
    #     df = df[["Open", "Close", "High", "Low", "Volume", "Dividends"]]
    #     df.to_csv(f"{RAW_STOCKS}/USA/{name}.csv")
    #     df_pct = df["Close"].pct_change()
    #     df_pct.to_csv(f"{STOCKS_DIFF}/USA/{name}.csv")

    tv = TvDatafeed(tvdatafeed_user, tvdatafeed_password, chromedriver_path=None)

    for name in ftse_100_tickers:
        df = tv.get_hist(name, exchange='LSE', interval=Interval.in_daily, n_bars=6000)
        if df is None:
            continue
        df.rename(columns={'open': 'Open', 'close': 'Close', 'high': 'High', 'low': 'Low', 'volume': 'Volume'}, inplace=True)
        df = df.loc['2000-01-01':'2023-01-01', ["Open", "Close", "High", "Low", "Volume"]]
        df.index = df.index.date
        df.index.name = "Date"
        name += ".L"
        print(name)
        t = yf.Ticker(name)
        ydf = t.history(start='2000-01-01', end='2023-01-01')
        ydf.index = ydf.index.date
        if ydf.shape[0] == 0:
            continue
        df["Dividends"] = ydf["Dividends"]
        df.to_csv(f"{RAW_STOCKS}/UK/{name}.csv")
        df_pct = df["Close"].pct_change()
        df_pct.to_csv(f"{STOCKS_DIFF}/UK/{name}.csv")

    for name in imoex_tickers:
        df = tv.get_hist(name, exchange='MOEX', interval=Interval.in_daily, n_bars=6000)
        if df is None:
            continue
        df.rename(columns={'open': 'Open', 'close': 'Close', 'high': 'High', 'low': 'Low', 'volume': 'Volume'},
                  inplace=True)
        df = df.loc['2000-01-01':'2023-01-01', ["Open", "Close", "High", "Low", "Volume"]]
        df.index = df.index.date
        df.index.name = "Date"
        name += ".ME"
        print(name)
        t = yf.Ticker(name)
        ydf = t.history(start='2000-01-01', end='2023-01-01')
        if ydf.shape[0] == 0:
            continue
        ydf.index = ydf.index.date
        df["Dividends"] = ydf["Dividends"]
        df.to_csv(f"{RAW_STOCKS}/Russia/{name}.csv")
        df_pct = df["Close"].pct_change()
        df_pct.to_csv(f"{STOCKS_DIFF}/Russia/{name}.csv")

    for name in hk35_tickers:
        df = tv.get_hist(name, exchange='HKEX', interval=Interval.in_daily, n_bars=6000)
        if df is None:
            continue
        df.rename(columns={'open': 'Open', 'close': 'Close', 'high': 'High', 'low': 'Low', 'volume': 'Volume'},
                  inplace=True)
        df = df.loc['2000-01-01':'2023-01-01', ["Open", "Close", "High", "Low", "Volume"]]
        df.index = df.index.date
        df.index.name = "Date"
        name = '0' * (4 - len(name)) + name + '.HK'
        print(name)
        t = yf.Ticker(name)
        ydf = t.history(start='2000-01-01', end='2023-01-01')
        if ydf.shape[0] == 0:
            continue
        ydf.index = ydf.index.date
        df["Dividends"] = ydf["Dividends"]
        df.to_csv(f"{RAW_STOCKS}/China/{name}.csv")
        df_pct = df["Close"].pct_change()
        df_pct.to_csv(f"{STOCKS_DIFF}/China/{name}.csv")

