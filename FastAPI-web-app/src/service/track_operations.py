from typing import Any

from fastapi import UploadFile
from src.models.enumerations import TrackFields

from src.repository import tracks_repository
from src.models.models import ScoredTrack, Track, UploadedTrack
from src.service import classification_model, feature_extraction
from src.utils import model_creation


def get_tracks(
    offset: int,
    limit: int,
    track_listens_lower_bound: int | None,
    track_listens_upper_bound: int | None,
    exact_match_filter: dict[str, Any] = None,
) -> tuple[list[Track], int | None]:
    """
    Retrieve a list of tracks based on various filters.

    Args:
        offset (int): The starting index for pagination.
        limit (int): The maximum number of tracks to retrieve.
        track_listens_lower_bound (int | None): Lower bound for track listens count filter.
        track_listens_upper_bound (int | None): Upper bound for track listens count filter.
        exact_match_filter (dict[str, Any]): Filters for exact matches on track attributes. Default is None.

    Returns:
        tuple[list[Track], int | None]: A tuple containing a list of Track objects and the next page's track ID.

    """

    tracks, next_page_track_id = tracks_repository.get_tracks(
        offset=offset,
        limit=limit,
        track_listens_lower=track_listens_lower_bound,
        track_listens_upper=track_listens_upper_bound,
        exact_match_filter=exact_match_filter,
    )
    return (
        [model_creation.record_to_track(record) for record in tracks],
        next_page_track_id,
    )


def get_tracks_by_full_text_match(
    match_string: str, offset: int, limit: int | None, enum_field: TrackFields
) -> list[Track]:
    """
    Retrieve tracks that have a full-text match with a given string in a specified field.

    Args:
        match_string (str): The string to match against in the specified field.
        offset (int): The offset for paginating results.
        limit (int | None): The maximum number of tracks to retrieve. Set to None to retrieve all matching tracks.
        enum_field (TrackFields): The field in which to search for a full-text match.

    Returns:
        list[Track]: A list of Track objects that match the search criteria.
    """

    tracks, _ = tracks_repository.get_tracks_full_text_match(
        match_string=match_string,
        offset=offset,
        limit=tracks_repository.get_number_of_datapoints() if not limit else limit,
        enum_field=enum_field,
    )
    return [model_creation.record_to_track(record) for record in tracks]


def find_n_most_similar_tracks_by_id(
    track_id: int, n: int, exact_match_filter: dict[str, Any] | None = None
) -> list[ScoredTrack]:
    """
    Find the top N most similar tracks to a track by its ID.

    Args:
        track_id (int): The ID of the track to find similar tracks for.
        n (int): The number of similar tracks to retrieve.
        exact_match_filter (dict[str, Any] | None): A dictionary specifying exact match filters for query clauses.
            Set to None if no exact match filters are needed.

    Returns:
        list[ScoredTrack]: A list of ScoredTrack objects representing the most similar tracks found.
    """

    return [
        model_creation.record_to_track(scored_point)
        for scored_point in tracks_repository.get_most_similar_tracks(
            track_id=track_id,
            limit=n,
            with_payload=True,
            exact_match_filter=exact_match_filter,
        )
    ]


def find_n_most_similar_tracks_by_embedding(
    track_embedding: list[float], n: int
) -> list[ScoredTrack]:
    """
    Find the top N most similar tracks based on a given track embedding.

    Args:
        track_embedding (list[float]): The embedding vector of the track to find similar tracks for.
        n (int): The number of similar tracks to retrieve.

    Returns:
        list[ScoredTrack]: A list of ScoredTrack objects representing the most similar tracks found.
    """

    return [
        model_creation.record_to_track(scored_point)
        for scored_point in tracks_repository.get_most_similar_tracks(
            track_embedding=track_embedding,
            limit=n,
            with_payload=True,
        )
    ]


def get_track_by_id(track_id: int) -> Track:
    """
    Retrieve a track by its ID.

    Args:
        track_id (int): The unique identifier of the track.

    Returns:
        Track: The retrieved track as a Track object.

    """

    return model_creation.record_to_track(
        tracks_repository.get_track_by_id(track_id=track_id)
    )


async def clf_and_most_similar_tracks(
    file: UploadFile, top_n_genres: int, top_n_similar: int
) -> UploadedTrack:
    """
    Perform genre prediction and find the most similar tracks for an uploaded track file.

    Args:
        file (UploadFile): The uploaded track file for analysis.
        top_n_genres (int): The number of top genres to predict.
        top_n_similar (int): The number of most similar tracks to retrieve.

    Returns:
        UploadedTrack: An UploadedTrack object containing the most similar tracks and genre predictions.
    """

    track_x = await feature_extraction.extract_features(file)

    # Genre Prediction
    track_genre_distribution = classification_model.classify_track(track_x)
    top_n_genres_present = classification_model.get_top_n_genres_present(
        track_y=track_genre_distribution, top_n=top_n_genres
    )

    # Similarity Search
    most_similar_tracks = find_n_most_similar_tracks_by_embedding(
        track_x.values[0], top_n_similar
    )

    return UploadedTrack(
        most_similar_tracks=most_similar_tracks, genre_prediction=top_n_genres_present
    )
