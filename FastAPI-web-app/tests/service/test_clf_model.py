import pandas as pd
import pytest

from src.utils import constants
from src.utils.feature_extraction import generate_columns
from src.service import classification_model


def test_make_prediction__given_valid_dataframe_cols_ordering__returns_pred_proba():
    # given
    multi_index = generate_columns()
    x = pd.DataFrame([[0] * constants.EMBEDDINGS_DIMENSIONALITY])
    x.columns = multi_index
    # this is the correct ordering on which the model was trained
    x = x[constants.SCALER_FEATURES_ORDER]

    # when
    y = classification_model.classify_track(x)

    # then
    assert (
        y.columns.values.tolist() == constants.CLASS_NAMES_MODEL_ORDER
    ), """Incorrect genre ordering"""
    assert (
        y.shape[1] == 16
    ), """The number of columns should correspond to the number of genres - 16"""


def test_make_prediction__given_df_mixed_cols_ordering__raises_exception():
    # given
    multi_index = generate_columns()
    x = pd.DataFrame([[0] * constants.EMBEDDINGS_DIMENSIONALITY])
    x.columns = multi_index

    # when/then
    with pytest.raises(ValueError):
        classification_model.classify_track(x)


def test_get_genres__given_predict_proba__returns_top_n_genres():
    # given
    y = pd.DataFrame([[0.2, 0.3, 0.4, 0.1]])

    # when
    top_n_genres = classification_model.get_top_n_genres_present(y, top_n=2)

    # then
    assert len(top_n_genres.items()) == 2, """Returned more genres than specified"""
    assert list(map(lambda t: t[1], top_n_genres.items())) == [
        40.0,
        30.0,
    ], """Values are not percentages"""
