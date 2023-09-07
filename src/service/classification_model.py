import pandas as pd
import tensorflow as tf

from src.utils import constants


def classify_track(track_x: pd.DataFrame) -> pd.DataFrame:
    # Loading the model
    mlp_clf = tf.keras.models.load_model(constants.MODEL_SERIAZLIATION_PATH)

    # Making the prediction
    track_y = pd.DataFrame(
        mlp_clf.predict(track_x.values, verbose=0),
        columns=constants.CLASS_NAMES_MODEL_ORDER,
        index=track_x.index,
    )

    return track_y


def get_top_n_genres_present(
        track_y: pd.DataFrame, 
        top_n: int = 5
    ) -> dict[str, float]:

    """
    Get the top N genres present in the prediction.

    Args:
        track_y (pd.DataFrame): A DataFrame of genre probabilities.
        top_n (int, optional): The number of top genres to return. Defaults to 5.

    Returns:
        dict[str, float]: A dictionary mapping genre names to their probabilities.
    """

    track_y = track_y.iloc[0, :]
    track_y = track_y * 100
    return track_y.sort_values(ascending=False)[:top_n].to_dict()
