import os

from typing import Any

from dotenv import load_dotenv
from qdrant_client import QdrantClient, models
from qdrant_client.http.models.models import Record, ScoredPoint

from src.models.exceptions.database_error_exception import DatabaseError
from src.utils.repo_utils import generate_must_clauses

load_dotenv()
COLLECTION_NAME = os.getenv('QDRANT_COLLECTION_NAME')
client = QdrantClient(url=os.getenv('QDRANT_URL'))


def get_tracks(
        offset: int = 0,
        limit: int = 15,
        exact_match_filter: dict[str, Any] = None,
        track_listens_lower: int | None = None,
        track_listens_upper: int | None = None
    ) -> tuple[list[Record], int | None]:

    """
    Retrieve a list of tracks based on various filters.

    Args:
        offset (int): The starting index for pagination. Default is 0.
        limit (int): The maximum number of tracks to retrieve. Default is 15.
        exact_match_filter (dict[str, Any]): Filters for exact matches on track attributes. Default is None. Format of entries: (attribute_name, value)
        track_listens_lower (int | None): Lower bound for track listens count filter. Default is None.
        track_listens_upper (int | None): Upper bound for track listens count filter. Default is None.

    Returns:
        tuple[list[Record], int | None]: A tuple containing a list of records (tracks) and the index of the track on the next page.
    """

    must_clauses = generate_must_clauses(exact_match_filter) + [
        models.FieldCondition(
            key='meta_track_listens', 
            range=models.Range(
                gt=track_listens_lower,
                lt=track_listens_upper
            )
        )
    ] 
    
    return client.scroll(
        collection_name=COLLECTION_NAME,
        offset=offset,
        limit=limit,
        scroll_filter=models.Filter(
            must=must_clauses
        ),
        with_payload=True,
        with_vectors=False
    )


def get_track_by_id(
        track_id: int, 
        with_payload: bool = True, 
        with_vectors: bool = False
    ) -> Record | None:

    """
    Retrieve a track by its ID.

    Args:
        track_id (int): The unique identifier of the track.
        with_payload (bool): Whether to include payload in the response. Default is True.
        with_vectors (bool): Whether to include vectors in the response. Default is False.

    Returns:
        Record | None: The retrieved track as a Record object, or None if the track doesn't exist.
    """

    tracks: list[Record] = client.retrieve(
        collection_name=COLLECTION_NAME,
        ids=[track_id],
        with_payload=with_payload,
        with_vectors=with_vectors
    )
    # the DB would not allow duplicate indexes
    if len(tracks) == 1:
        return tracks[0]
    elif len(tracks) == 0:
        return None
    else:
        raise DatabaseError('Multiple tracks with the same ID found.') 


def get_most_similar_tracks(
        track_id: int, 
        limit: int = 10, 
        exact_search: bool = False,
        with_payload: bool = True, 
        with_vectors: bool = False,
        exact_match_filter: dict[str, Any] | None = None
    ) -> list[ScoredPoint]:

    """
    Retrieve a list of tracks similar to a given track.

    Args:
        track_id (int): The unique identifier of the query track.
        limit (int): The maximum number of similar tracks to retrieve. Default is 10.
        exact_search (bool): Whether to perform an exact search. Default is False.
        with_payload (bool): Whether to include payload in the response. Default is True.
        with_vectors (bool): Whether to include vectors in the response. Default is False.
        exact_match_filter (dict[str, Any] | None): Filters for exact matches on track attributes. Default is None.

    Returns:
        list[ScoredPoint]: A list of ScoredPoint objects representing similar tracks.
    """

    query_track = get_track_by_id(track_id=track_id, with_payload=False, with_vectors=True)

    if query_track is None:
        raise DatabaseError(f'Track with id: {track_id} does not exist.')

    must_clauses = generate_must_clauses(exact_match_filter)

    return client.search(
        collection_name=COLLECTION_NAME,
        query_vector=query_track.vector,
        query_filter=models.Filter(must=must_clauses),
        search_params=models.SearchParams(exact=exact_search),
        limit=limit,
        with_vectors=with_vectors,
        with_payload=with_payload
    )


