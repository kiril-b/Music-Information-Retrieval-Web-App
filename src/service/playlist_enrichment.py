from src.models.models import Track
import numpy as np
from qdrant_client.http.models.models import Record, ScoredPoint

from src.repository import tracks_repository
from src.utils import model_creation


def enrich(track_ids: list[int]) -> list[Track]:
    """
    Enriches a playlist by finding and adding similar tracks for each given track ID.

    Args:
        track_ids (list[int]): A list of track IDs for which to enrich the playlist.

    Returns:
        list[Track]: A list of Track objects representing the enriched playlist.

    Note:
        This is a demo function for playlist enrichment and will be modified
        to include more meaningful playlist enrichment in the future.
    """

    enriched_playlist_points: list[ScoredPoint] = list()
    for track_id in track_ids:
        most_similar_for_track = tracks_repository.get_most_similar_tracks(
            track_id=track_id,
            limit=6,
            exact_search=False,
            with_payload=True,
            with_vectors=False,
        )
        # The first result will be the same song as the query
        query_point = most_similar_for_track.pop(0)
        # Append the track given in the query
        enriched_playlist_points.append(query_point)
        # Choose the number of similar tracks to consider
        num_tracks = np.random.randint(1, 6)
        # Append the new points similar to the one in the query
        enriched_playlist_points += np.random.choice(
            most_similar_for_track, num_tracks, replace=False
        ).tolist()

    return [
        Track(**model_creation.record_to_track(scored_point).dict())
        for scored_point in enriched_playlist_points
    ]
