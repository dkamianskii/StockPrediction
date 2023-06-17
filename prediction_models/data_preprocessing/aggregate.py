import pandas as pd
import numpy as np
from prediction_models.config import STOCKS_PREPROCESSED, STOCK_AGG, val_start_date, test_start_date
import os


def one_observe():
    countries = ["USA", "UK", "Russia", "China"]
    x_trains = []
    y_trains = {"1": [], "2": [], "3": []}
    x_vals = {"1": [], "2": [], "3": []}
    y_vals = {"1": [], "2": [], "3": []}

    for country in countries:
        print(country)
        data_files = os.listdir(f"{STOCKS_PREPROCESSED}/{country}")
        for data_file in data_files:
            data = pd.read_csv(f"{STOCKS_PREPROCESSED}/{country}/{data_file}", index_col="Date", parse_dates=['Date'])
            data = data[:test_start_date]
            target = pd.DataFrame()
            for i in range(1, 10):
                target[f"t-{i}"] = data["Close"].shift(-i)
            train_data = data[:val_start_date]
            x_trains.append(train_data)
            val_data = data[val_start_date:]
            train_target = target[:val_start_date]
            val_target = target[val_start_date:]
            for i in range(3):
                y_trains[f"{i + 1}"].append(train_target[[f"t-{i * 3 + 1}", f"t-{i * 3 + 2}", f"t-{i * 3 + 3}"]])
                y_vals[f"{i + 1}"].append(
                    val_target[[f"t-{i * 3 + 1}", f"t-{i * 3 + 2}", f"t-{i * 3 + 3}"]][:-3 * (i + 1)])
                x_vals[f"{i + 1}"].append(val_data[:-3 * (i + 1)])
    x_train = pd.concat(x_trains)
    x_train.to_csv(f"{STOCK_AGG}\\X_train_S1.csv")
    for i in range(3):
        x_val = pd.concat(x_vals[f"{i + 1}"])
        x_val.to_csv(f"{STOCK_AGG}\\X_val_{i + 1}_S1.csv")
        y_val = pd.concat(y_vals[f"{i + 1}"])
        y_val.to_csv(f"{STOCK_AGG}\\y_val_{i + 1}_S1.csv")
        y_train = pd.concat(y_trains[f"{i + 1}"])
        y_train.to_csv(f"{STOCK_AGG}\\y_train_{i + 1}_S1.csv")


def multiple_observes(num_of_observes):
    countries = ["USA", "UK", "Russia", "China"]
    x_trains = []
    y_trains = {"1": [], "2": [], "3": []}
    x_vals = {"1": [], "2": [], "3": []}
    y_vals = {"1": [], "2": [], "3": []}

    for country in countries:
        print(country)
        data_files = os.listdir(f"{STOCKS_PREPROCESSED}/{country}")
        for data_file in data_files:
            data = pd.read_csv(f"{STOCKS_PREPROCESSED}/{country}/{data_file}", index_col="Date", parse_dates=['Date'])
            data = data[:test_start_date]
            target = pd.DataFrame()
            for i in range(1, 10):
                target[f"t-{i}"] = data["Close"].shift(-i)
            target = target[num_of_observes:]
            x = []
            for i in range(data.shape[0] - num_of_observes):
                x.append(data[i:i + num_of_observes].to_numpy().flatten())
            if len(x) == 0:
                continue
            x = np.array(x)
            val_indx = data[:val_start_date].shape[0]
            train_data = x[:val_indx]
            x_trains.append(train_data)
            val_data = x[val_indx:]
            train_target = target[:val_indx]
            val_target = target[val_indx:]
            for i in range(3):
                y_trains[f"{i + 1}"].append(train_target[[f"t-{i * 3 + 1}", f"t-{i * 3 + 2}", f"t-{i * 3 + 3}"]])
                y_vals[f"{i + 1}"].append(
                    val_target[[f"t-{i * 3 + 1}", f"t-{i * 3 + 2}", f"t-{i * 3 + 3}"]][:-3 * (i + 1)])
                x_vals[f"{i + 1}"].append(val_data[:-3 * (i + 1)])
    x_train = pd.DataFrame(np.concatenate(x_trains))
    x_train.to_csv(f"{STOCK_AGG}\\X_train_S{num_of_observes}.csv")
    for i in range(3):
        x_val = pd.DataFrame(np.concatenate(x_vals[f"{i + 1}"]))
        x_val.to_csv(f"{STOCK_AGG}\\X_val_{i + 1}_S{num_of_observes}.csv")
        y_val = pd.concat(y_vals[f"{i + 1}"])
        y_val.to_csv(f"{STOCK_AGG}\\y_val_{i + 1}_S{num_of_observes}.csv")
        y_train = pd.concat(y_trains[f"{i + 1}"])
        y_train.to_csv(f"{STOCK_AGG}\\y_train_{i + 1}_S{num_of_observes}.csv")


if __name__ == "__main__":
    multiple_observes(10)
