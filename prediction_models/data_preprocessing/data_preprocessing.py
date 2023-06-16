import pandas as pd
import yfinance as yf
import ta
import os
from prediction_models.config import RAW_STOCKS, STOCKS_PREPROCESSED


def create_learning_data():
    sp500_tickers = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')[0]['Symbol'].tolist()
    hk35_tickers = ['0001.HK', '0002.HK', '0003.HK', '0005.HK', '0006.HK', '0008.HK', '0011.HK', '0012.HK', '0016.HK',
                    '0017.HK', '0019.HK',
                    '0027.HK', '0066.HK', '0101.HK', '0288.HK', '0267.HK', '0293.HK', '0316.HK', '0388.HK', '0522.HK',
                    '0669.HK', '0823.HK',
                    '0853.HK', '1038.HK', '1113.HK', '1299.HK', '1308.HK', '1928.HK', '1972.HK', '1997.HK', '2269.HK',
                    '2388.HK', '2888.HK', '6969.HK']
    imoex_tickers = ['AFKS.ME', 'AFLT.ME', 'ALRS.ME', 'AGRO.ME', 'CHMF.ME', 'ENPG.ME', 'FIVE.ME', 'FIXP.ME', 'GLTR.ME',
                     'GAZP.ME', 'GMKN.ME',
                     'HYDR.ME', 'IRAO.ME', 'LKOH.ME', 'MAGN.ME', 'MGNT.ME', 'MTSS.ME', 'NLMK.ME', 'NVTK.ME', 'OZON.ME',
                     'PHOR.ME', 'ROSN.ME',
                     'RTKM.ME', 'PLZL.ME', 'POLY.ME', 'RUAL.ME', 'TCSG.ME', 'VKCO.ME', 'YNDX.ME', 'SBER.ME', 'SNGS.ME',
                     'TATN.ME', 'TRNFP.ME', 'VTBR.ME']
    ftse_100_ticker = pd.read_html('https://en.wikipedia.org/wiki/FTSE_100_Index#Constituents')[4]['Ticker'].tolist()
    for i in range(len(ftse_100_ticker)):
        ftse_100_ticker[i] += '.L'

    for ticker in sp500_tickers:
        t = yf.Ticker(ticker)
        df = t.history(start='2000-01-01', end='2021-12-31')
        process_stock_data(df, ticker, "USA")

    for ticker in ftse_100_ticker:
        t = yf.Ticker(ticker)
        df = t.history(start='2000-01-01', end='2021-12-31')
        process_stock_data(df, ticker, "UK")

    for ticker in imoex_tickers:
        t = yf.Ticker(ticker)
        df = t.history(start='2000-01-01', end='2021-12-31')
        process_stock_data(df, ticker, "Russia")

    for ticker in hk35_tickers:
        t = yf.Ticker(ticker)
        df = t.history(start='2000-01-01', end='2021-12-31')
        process_stock_data(df, ticker, "China")


def process_stock_data(df, country) -> pd.DataFrame:
    df_final = df[["High", "Low", "Open", "Close"]].pct_change().copy()
    df_final["Volume"] = (df["Volume"] - df["Volume"].rolling(50).median()) / df["Volume"]

    ema_periods = [20, 30, 50, 100, 200]
    for period in ema_periods:
        df_final[f"EMA {period}"] = (df["Close"] - ta.trend.ema_indicator(df['Close'], window=period)) / df["Close"]

    min_max_close_periods = [50, 100, 200]
    for period in min_max_close_periods:
        df_final[f"Max {period}"] = (df["Close"].rolling(period).max() - df["Close"]) / df["Close"]
        df_final[f"Min {period}"] = (df["Close"] - df["Close"].rolling(period).min()) / df["Close"]

    std_periods = [25, 50, 100]
    for period in std_periods:
        df_final[f"Std {period}"] = df["Close"].rolling(period).std() / df["Close"]

    atr_periods = [14, 28, 56]
    for period in atr_periods:
        df_final[f"ATR {period}"] = ta.volatility.average_true_range(df["High"], df["Low"], df["Close"],
                                                                     window=period) / df["Close"]

    df_final["RSI"] = ta.momentum.rsi(df["Close"]) / 100
    df_final["MACD diff"] = ta.trend.macd_diff(df["Close"])
    df_final["Stochastic Oscilator"] = ta.momentum.StochasticOscillator(df["High"], df["Low"],
                                                                        df["Close"]).stoch() / 100
    df_final["A/D line change"] = ta.volume.acc_dist_index(df["High"], df["Low"], df["Close"],
                                                           df["Volume"]).pct_change()
    df_final["CCI"] = ta.trend.cci(df["High"], df["Low"], df["Close"]) / 100

    df['Day of week'] = [d.weekday() for d in df.index]
    df_final[["Mon", "Tues", "Wed", "Thurs", "Fri"]] = 0
    df_final.loc[df['Day of week'] == 0, "Mon"] = 1
    df_final.loc[df['Day of week'] == 1, "Tues"] = 1
    df_final.loc[df['Day of week'] == 2, "Wed"] = 1
    df_final.loc[df['Day of week'] == 3, "Thurs"] = 1
    df_final.loc[df['Day of week'] == 4, "Fri"] = 1

    day_before = df.shift(-1).iloc[:-1]
    before_div = day_before['Dividends'] != 0
    df_final["Day before div"] = 0
    df_final["Div day"] = 0
    df_final.loc[day_before[before_div].index, "Day before div"] = 1
    df_final.loc[df['Dividends'] != 0, 'Div day'] = 1
    df_final["Rel div"] = df['Dividends'] / df['Close']
    rel_div = day_before[before_div]["Dividends"] / day_before[before_div]["Close"]
    df_final.loc[day_before[before_div].index, "Day before div"] = rel_div

    df_final[["USA", "UK", "Russia", "China"]] = 0
    df_final.loc[:, country] = 1

    df_final.dropna(inplace=True)
    return df_final


if __name__ == "__main__":
    countries = ["USA"]

    for country in countries:
        print(country)
        data_files = os.listdir(f"{RAW_STOCKS}/{country}")
        for data_file in data_files:
            data = pd.read_csv(f"{RAW_STOCKS}/{country}/{data_file}", index_col="Date", parse_dates=['Date'])
            if data.index[0].year > 2017:
                print(data_file[:-4] + " too short")
                continue
            print(data_file[:-4])
            df = process_stock_data(data, country)
            df.to_csv(f"{STOCKS_PREPROCESSED}/{country}/{data_file[:-4]}.csv")

