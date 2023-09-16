import io

import joblib
import librosa
import numpy as np
import pandas as pd
from fastapi import UploadFile

from src.utils import constants
from src.utils.feature_extraction import feature_stats, generate_columns


async def extract_features(file: UploadFile, scale: bool = True) -> pd.DataFrame:
    contents = await file.read()
    audio_data, sample_rate = librosa.load(io.BytesIO(contents), sr=None, mono=True)

    (
        chroma,
        zcr,
        rmse,
        spectral_contrast,
        spectral_rolloff,
        mfcc,
    ) = extract_audio_features_raw(audio_data, sample_rate)

    features_df = raw_features_to_df(
        file.filename, chroma, zcr, rmse, spectral_contrast, spectral_rolloff, mfcc
    )

    if scale:
        standard_scaler = joblib.load(constants.SCALER_SERAZLIZATION_PATH)

        # The ordeding of the featues on which the scaler was fit
        features_ordered = features_df[constants.SCALER_FEATURES_ORDER]

        scaled_df = pd.DataFrame(
            standard_scaler.transform(features_ordered),
            index=features_ordered.index,
            columns=features_ordered.columns,
        )
        return scaled_df

    return features_df[constants.SCALER_FEATURES_ORDER]


def extract_audio_features_raw(
    audio_data: np.ndarray, sample_rate: float
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    chroma = extract_chroma_features(audio_data, sample_rate)
    zcr = librosa.feature.zero_crossing_rate(
        audio_data, frame_length=2048, hop_length=512
    )
    stft = np.abs(librosa.stft(audio_data, n_fft=2048, hop_length=512))
    rmse = librosa.feature.rms(S=stft)
    spectral_contrast = librosa.feature.spectral_contrast(S=stft, n_bands=6)
    spectral_rolloff = librosa.feature.spectral_rolloff(S=stft)
    mel = librosa.feature.melspectrogram(sr=sample_rate, S=stft**2)
    mfcc = librosa.feature.mfcc(S=librosa.power_to_db(mel), n_mfcc=20)

    return chroma, zcr, rmse, spectral_contrast, spectral_rolloff, mfcc


def extract_chroma_features(audio_data: np.ndarray, sample_rate: int) -> np.ndarray:
    cqt = np.abs(
        librosa.cqt(
            audio_data,
            sr=sample_rate,
            hop_length=512,
            bins_per_octave=12,
            n_bins=7 * 12,
            tuning=None,
        )
    )

    return librosa.feature.chroma_cqt(C=cqt, n_chroma=12, n_octaves=7)


def raw_features_to_df(
    track_name: str,
    chroma: np.ndarray,
    zcr: np.ndarray,
    rmse: np.ndarray,
    spectral_contrast: np.ndarray,
    spectral_rolloff: np.ndarray,
    mfcc: np.ndarray,
) -> pd.DataFrame:
    features = pd.Series(
        index=generate_columns(), dtype=np.float32, name=f"track_{track_name}"
    )

    features = feature_stats(features=features, name="chroma_cqt", values=chroma)
    features = feature_stats(features=features, name="zcr", values=zcr)
    features = feature_stats(features=features, name="rmse", values=rmse)
    features = feature_stats(features=features, name="spectral_contrast", values=spectral_contrast)  # noqa: E501
    features = feature_stats(features=features, name="spectral_rolloff", values=spectral_rolloff)  # noqa: E501
    features = feature_stats(features=features, name="mfcc", values=mfcc)

    features_df = features.to_frame().T
    return features_df
