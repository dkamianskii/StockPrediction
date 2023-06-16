import pandas as pd
import numpy as np
from pmdarima.arima import ARIMA, auto_arima
from prediction_models.config import MODELS_DIRECTORY, STOCKS_DIFF, train_start_date, test_start_date, test_end_date, random_state
import pickle
import concurrent
import os
from concurrent import futures


def process_arima(country_symbol):
    time_frames = [200, 100, 50, 20]
    df = pd.read_csv(f"{STOCKS_DIFF}/{country_symbol[0]}/{country_symbol[1]}", index_col="Date", parse_dates=['Date'])
    df = df[1:]
    data_train = df.loc[train_start_date:test_start_date]["Close"]
    time_frame_errors = {}
    for time_frame in time_frames:
        if data_train.shape[0] + 6 < time_frame:
            continue
        errors = []
        for i in range(0, data_train.shape[0] - time_frame - 6, 10):
            mod: ARIMA = auto_arima(y=data_train[i:i + time_frame], start_p=2, start_q=2, max_p=4, max_q=4, max_d=1, max_order=8,
                                    with_intercept=True,
                                    seasonal=False, error_action="ignore", random_state=random_state)
            predicts = np.array(mod.predict(6))
            pred_err = (predicts - data_train[i + time_frame:i + time_frame + 6]) ** 2
            errors += pred_err.to_list()
        time_frame_errors[time_frame] = np.array(errors).mean()
    best_time_frame = min(time_frame_errors, key=time_frame_errors.get)
    test_predicts = []
    test_data_time = data_train.index[-best_time_frame]
    data_test = df.loc[test_data_time:]
    for i in range(data_test.shape[0] - best_time_frame - 5):
        mod: ARIMA = auto_arima(y=data_train[i:i + best_time_frame], start_p=2, start_q=2, max_p=4, max_q=4, max_d=1,
                                max_order=8, with_intercept=True,
                                seasonal=False, error_action="ignore", random_state=random_state)
        predicts = np.array(mod.predict(6))
        test_predicts.append(predicts)
    result_dict = {"time_frame_errors": time_frame_errors,
                   "best_time_frame": best_time_frame,
                   "predicts": test_predicts}
    file_to_save = MODELS_DIRECTORY + f"\\arima\\results\\{country_symbol[0]}\\{country_symbol[1][:-4]}.pickle"
    with open(file_to_save, 'wb') as handle:
        pickle.dump(result_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)


if __name__ == "__main__":
    countries = ["USA", "UK", "Russia", "China"]
    country_symbols = []
    for country in countries:
        data_files = os.listdir(f"{STOCKS_DIFF}/{country}")
        for f in data_files:
            country_symbols.append((country, f))

    with concurrent.futures.ProcessPoolExecutor() as executor:
        executor.map(process_arima, country_symbols)


