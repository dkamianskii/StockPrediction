import xgboost as xg
import pandas as pd
from prediction_models.config import STOCK_AGG, random_state
import mlflow
import numpy as np
from multiprocessing import Process
import concurrent.futures


def train_xgboost_model(process_input):
    params, forecast_range, name = process_input
    mlflow.xgboost.autolog(disable=True)
    with mlflow.start_run(run_name=name):
        X = pd.read_csv(f"{STOCK_AGG}\\X_train_S10.csv")
        y = pd.read_csv(f"{STOCK_AGG}\\y_train_{forecast_range}_S10.csv", index_col="Date", parse_dates=['Date'])
        X_val = pd.read_csv(f"{STOCK_AGG}\\X_val_{forecast_range}_S10.csv")
        y_val = pd.read_csv(f"{STOCK_AGG}\\y_val_{forecast_range}_S10.csv", index_col="Date", parse_dates=['Date'])
        mlflow.set_tag("model_type", "XGboost S10")
        mlflow.set_tag("forecast_range", forecast_range)
        xgr = xg.XGBRegressor(eval_metric=['rmse', 'mae'],
                              tree_method='gpu_hist', gpu_id=0,
                              random_state=random_state)
        mlflow.log_params(params)
        xgr.set_params(**params)
        xgr.fit(X, y, eval_set=[(X, y), (X_val, y_val)], early_stopping_rounds=10)
        results = xgr.evals_result()
        mlflow.log_metric("best_ntree_limit", xgr.best_ntree_limit)
        for i in range(len(results["validation_0"]["rmse"])):
            mlflow.log_metric("rmse_train", results["validation_0"]["rmse"][i], i)
            mlflow.log_metric("rmse_val", results["validation_1"]["rmse"][i], i)
            mlflow.log_metric("mae_train", results["validation_0"]["mae"][i], i)
            mlflow.log_metric("mae_val", results["validation_1"]["mae"][i], i)
        predictions = xgr.predict(X_val, iteration_range=(0, xgr.best_iteration + 1))
        err = ((y_val - predictions) ** 2).to_numpy()
        err_for_day = np.sqrt(err.mean(axis=0))
        err_total = np.sqrt(err.mean())
        mlflow.log_metric("final_val_rmse", err_total)
        for i in range(len(err_for_day)):
            mlflow.log_metric("rmse_in_forecast_range", err_for_day[i], i + 1)


if __name__ == "__main__":
    params_versions = []
    np.random.seed(random_state)
    for _ in range(1):
        params = {"n_estimators": np.random.randint(300, 1501),
                  "max_depth": np.random.randint(3, 21),
                  "learning_rate": np.random.choice([0.1, 0.01, 0.005, 0.001]),
                  "subsample": np.random.choice([1, 0.75, 0.5, 0.25]),
                  "colsample_bytree": np.random.choice([1, 0.75, 0.5, 0.25])}
        params_versions.append(params)

    inputs = []
    for i in range(1, 2):
        for j in range(len(params_versions)):
            inputs.append((params_versions[j], i, f"xgboost S10 r{i} {j}"))

    train_xgboost_model(inputs[0])

    # with concurrent.futures.ProcessPoolExecutor(max_workers=4) as executor:
    #     executor.map(train_xgboost_model, inputs)
    # fitting_process = Process(target=train_xgboost_model, args=(params_versions[1], 2, "xgboost r2 1"))
    # fitting_process.start()
    # fitting_process.join()
