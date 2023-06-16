import numpy as np


def direction_accuracy(predictions: np.ndarray, targets: np.ndarray) -> float:
    predictions = predictions[:, :, 1]
    sign_pred: np.ndarray = np.sign(predictions)
    sign_targets: np.ndarray = np.sign(targets)
    coincidence: np.ndarray = sign_pred == sign_targets
    element_wise_acc = coincidence.sum(axis=1)
    return element_wise_acc.mean()


def excess_frequency(predictions: np.ndarray, targets: np.ndarray) -> float:
    pos_excess = (targets - predictions[:, :, 0]) > 0
    neg_excess = ( predictions[:, :, 2] - targets) < 0
    excess = (pos_excess | neg_excess)
    return excess.sum() / (excess.shape[0] * excess.shape[1])


def forecast_horizon_overlap(predictions: np.ndarray, targets: np.ndarray) -> float:
    target_pos_excess = targets - predictions[:, :, 0]
    target_pos_excess = target_pos_excess[target_pos_excess > 0]
    target_neg_excess = predictions[:, :, 2] - targets
    target_neg_excess = np.abs(target_neg_excess[target_neg_excess < 0])
    mean_excesses = np.concatenate((target_pos_excess, target_neg_excess)).mean()
    mean_width = np.abs(predictions[:, :, 0] - predictions[:, :, 2]).mean()
    return 1 / ((1 + mean_excesses) * (1 + mean_width))
