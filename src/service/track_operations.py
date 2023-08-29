from typing import Any

from src.repository import tracks_repository
from src.models.models import ScoredTrack, Track
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
                exact_match_filter=exact_match_filter
            )
    return ([model_creation.record_to_track(record) for record in tracks], next_page_track_id)



def find_n_most_similar_tracks(track_id: int, n: int, exact_match_filter: dict[str, Any] | None = None) -> list[ScoredTrack]:
    
    """
    Find the n most similar tracks to a given track.

    Args:
        track_id (int): The unique identifier of the query track.
        n (int): The number of similar tracks to retrieve.
        exact_match_filter (dict[str, Any] | None): Filters for exact matches on track attributes. Default is None.

    Returns:
        list[ScoredTrack]: A list of ScoredTrack objects representing the most similar tracks.

    """

    return [model_creation.record_to_track(scored_point) for scored_point in 
            tracks_repository.get_most_similar_tracks(
                track_id=track_id,
                limit=n,
                with_payload=True,
                exact_match_filter=exact_match_filter,
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

    return model_creation.record_to_track(tracks_repository.get_track_by_id(track_id=track_id))