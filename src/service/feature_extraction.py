import io
from fastapi import UploadFile
import librosa
import pandas as pd
import numpy as np

from src.utils.feature_extraction import feature_stats, generate_columns

async def extract_features(file: UploadFile) -> pd.Series:
    contents = await file.read()
    audio_data, sample_rate = librosa.load(io.BytesIO(contents), sr=None, mono=True)
    
    features = pd.Series(
        index=generate_columns(), 
        dtype=np.float32, 
        name=f'track_{file.filename}'
    )
    
    chroma, features = extract_chroma_features(audio_data, sample_rate, features)
    features = extract_tonnetz(chroma, features)
    features = extract_spectral_features(audio_data, sample_rate, features)

    print(features.shape)
    print(features.index)
    print(features.head())
    return features


def extract_chroma_features(
        audio_data: np.ndarray, 
        sample_rate: int, 
        features: pd.Series
    ) -> tuple[np.ndarray, pd.Series]:

    cqt = np.abs(librosa.cqt(
        audio_data, sr=sample_rate, hop_length=512, 
        bins_per_octave=12, n_bins=7*12, tuning=None))
    
    assert cqt.shape[0] == 7 * 12
    assert np.ceil(len(audio_data) / 512) <= cqt.shape[1] <= np.ceil(len(audio_data) / 512) + 1  # noqa: E501

    chroma = librosa.feature.chroma_cqt(C=cqt, n_chroma=12, n_octaves=7)

    return (chroma, feature_stats(
        features=features, 
        name='chroma_cqt', 
        values=chroma))


def extract_tonnetz(
        chroma: np.ndarray,
        features: pd.Series
    ) -> pd.Series:
    
    tonnetz = librosa.feature.tonnetz(chroma=chroma)
    return feature_stats(
        features=features,
        name='tonnetz',
        values=tonnetz
    )

def extract_spectral_features(
        audio_data: np.ndarray, 
        sample_rate: int, 
        features: pd.Series
    ) -> pd.Series:

    stft = np.abs(librosa.stft(audio_data, n_fft=2048, hop_length=512))

    assert stft.shape[0] == 1 + 2048 // 2
    assert np.ceil(len(audio_data) / 512) <= stft.shape[1] <= np.ceil(len(audio_data) / 512) + 1  # noqa: E501
    
    del audio_data

    f = librosa.feature.rms(S=stft)
    features = feature_stats(features, 'rmse', f)

    f = librosa.feature.spectral_centroid(S=stft)
    features = feature_stats(features, 'spectral_centroid', f)

    f = librosa.feature.spectral_bandwidth(S=stft)
    features = feature_stats(features, 'spectral_bandwidth', f)

    f = librosa.feature.spectral_contrast(S=stft, n_bands=6)
    features = feature_stats(features, 'spectral_contrast', f)

    f = librosa.feature.spectral_rolloff(S=stft)
    features = feature_stats(features, 'spectral_rolloff', f)

    mel = librosa.feature.melspectrogram(sr=sample_rate, S=stft**2)
    del stft

    f = librosa.feature.mfcc(S=librosa.power_to_db(mel), n_mfcc=20)
    features = feature_stats(features, 'mfcc', f)

    return features