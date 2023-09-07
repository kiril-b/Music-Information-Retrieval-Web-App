import io

import joblib
import librosa
import numpy as np
import pandas as pd
from fastapi import UploadFile

from src.utils import constants
from src.utils.feature_extraction import feature_stats, generate_columns


async def extract_features(file: UploadFile, scale: bool = True) -> pd.DataFrame:
    
    """
    Extract audio features from an uploaded audio file.

    Args:
        file (UploadFile): The uploaded audio file.
        scale (bool, optional): Whether to scale the extracted features. Defaults to True.

    Returns:
        pd.DataFrame: A DataFrame containing the extracted audio features.
    """  # noqa: E501

    contents = await file.read()
    audio_data, sample_rate = librosa.load(io.BytesIO(contents), sr=None, mono=True)
    
    features = pd.Series(
        index=generate_columns(), 
        dtype=np.float32, 
        name=f'track_{file.filename}'
    )
    
    features = extract_chroma_features(audio_data, sample_rate, features)
    features = extract_zero_crossing_rate(audio_data, features)
    features = extract_spectral_features(audio_data, sample_rate, features)

    features_df = features.to_frame().T

    if scale:
        standard_scaler = joblib.load(constants.SCALER_SERAZLIZATION_PATH)

        # The ordeding of the featues on which the scaler was fit
        features_ordered = features_df[constants.SCALER_FEATURES_ORDER]  # noqa: E501

        scaled_df = pd.DataFrame(
            standard_scaler.transform(features_ordered),
            index=features_df.index, 
            columns=features_df.columns
        )
        return scaled_df

    return features_df[constants.SCALER_FEATURES_ORDER]


def extract_chroma_features(
        audio_data: np.ndarray, 
        sample_rate: int, 
        features: pd.Series
    ) -> pd.Series:

    """
    Extract chroma features from audio data.

    Args:
        audio_data (np.ndarray): The audio data as a NumPy array.
        sample_rate (int): The sample rate of the audio.
        features (pd.Series): The pandas Series to store the extracted features.

    Returns:
        pd.Series: The updated pandas Series with chroma features.
    """

    cqt = np.abs(librosa.cqt(
        audio_data, sr=sample_rate, hop_length=512, 
        bins_per_octave=12, n_bins=7*12, tuning=None))
    
    assert cqt.shape[0] == 7 * 12
    assert np.ceil(len(audio_data) / 512) <= cqt.shape[1] <= np.ceil(len(audio_data) / 512) + 1  # noqa: E501

    chroma = librosa.feature.chroma_cqt(C=cqt, n_chroma=12, n_octaves=7)

    return feature_stats(
        features=features, 
        name='chroma_cqt', 
        values=chroma)


def extract_zero_crossing_rate(
        audio_data: np.ndarray,
        features: pd.Series
    ) -> pd.Series:

    """
    Extract zero-crossing rate feature from audio data.

    Args:
        audio_data (np.ndarray): The audio data as a NumPy array.
        features (pd.Series): The pandas Series to store the extracted features.

    Returns:
        pd.Series: The updated pandas Series with zero-crossing rate feature.
    """

    f = librosa.feature.zero_crossing_rate(audio_data, frame_length=2048, hop_length=512)
    return feature_stats(features, 'zcr', f)


def extract_spectral_features(
        audio_data: np.ndarray, 
        sample_rate: int, 
        features: pd.Series
    ) -> pd.Series:
    """
    Extract various spectral features from audio data and update the feature series.

    Args:
        audio_data (np.ndarray): The audio data as a NumPy array.
        sample_rate (int): The sample rate of the audio data.
        features (pd.Series): The feature series to update.

    Returns:
        pd.Series: The updated feature series.
    """

    stft = np.abs(librosa.stft(audio_data, n_fft=2048, hop_length=512))

    assert stft.shape[0] == 1 + 2048 // 2
    assert np.ceil(len(audio_data) / 512) <= stft.shape[1] <= np.ceil(len(audio_data) / 512) + 1  # noqa: E501
    
    del audio_data

    f = librosa.feature.rms(S=stft)
    features = feature_stats(features, 'rmse', f)

    f = librosa.feature.spectral_contrast(S=stft, n_bands=6)
    features = feature_stats(features, 'spectral_contrast', f)

    f = librosa.feature.spectral_rolloff(S=stft)
    features = feature_stats(features, 'spectral_rolloff', f)

    mel = librosa.feature.melspectrogram(sr=sample_rate, S=stft**2)
    del stft

    f = librosa.feature.mfcc(S=librosa.power_to_db(mel), n_mfcc=20)
    features = feature_stats(features, 'mfcc', f)

    return features