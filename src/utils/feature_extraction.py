import numpy as np
import pandas as pd
from scipy import stats


def generate_columns() -> pd.MultiIndex:
    """
    Generate a MultiIndex for feature columns.

    Returns:
        pd.MultiIndex: A MultiIndex containing column names for different audio features.
    """
    feature_sizes = dict(
        chroma_cqt=12, mfcc=20, rmse=1, zcr=1, spectral_contrast=7, spectral_rolloff=1
    )
    moments = ("mean", "std", "skew", "kurtosis", "median", "min", "max")

    columns = []
    for name, size in feature_sizes.items():
        for moment in moments:
            it = ((name, moment, "{:02d}".format(i + 1)) for i in range(size))
            columns.extend(it)

    names = ("feature", "statistics", "number")
    columns = pd.MultiIndex.from_tuples(columns, names=names)

    return columns.sort_values()


def feature_stats(features: pd.Series, name: str, values: np.ndarray) -> pd.Series:
    """
    Calculate statistics for audio features and update the feature series.

    Args:
        features (pd.Series): The feature series to update.
        name (str): The name of the feature.
        values (np.ndarray): The values of the feature.

    Returns:
        pd.Series: The updated feature series.
    """
    features[name, "min"] = np.min(values, axis=1)
    features[name, "max"] = np.max(values, axis=1)
    features[name, "mean"] = np.mean(values, axis=1)
    features[name, "std"] = np.std(values, axis=1)
    features[name, "median"] = np.median(values, axis=1)
    features[name, "skew"] = stats.skew(values, axis=1)
    features[name, "kurtosis"] = stats.kurtosis(values, axis=1)

    return features
