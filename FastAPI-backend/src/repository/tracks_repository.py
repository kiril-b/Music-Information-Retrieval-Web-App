import os

from typing import Any, cast

from dotenv import load_dotenv
from qdrant_client import QdrantClient, models
from qdrant_client.http.models.models import Record, ScoredPoint

from src.models.exceptions.exceptions import DatabaseError, InvalidAttributeCombination
from src.utils.repo_utils import generate_must_clauses
from src.models.enumerations import TrackFields

load_dotenv()
COLLECTION_NAME = os.environ["QDRANT_COLLECTION_NAME"]
client = QdrantClient(url=os.getenv("QDRANT_URL"))


def get_tracks(
    offset: int = 0,
    limit: int = 15,
    exact_match_filter: dict[str, Any] | None = None,
    track_listens_lower: int | None = None,
    track_listens_upper: int | None = None,
    client: QdrantClient = client,
    collection_name: str = COLLECTION_NAME,
) -> tuple[list[Record], int | None]:
    """
    Retrieve a list of tracks based on various filters.

    Args:
        offset (int): The starting index for pagination. Default is 0.
        limit (int): The maximum number of tracks to retrieve. Default is 15.
        exact_match_filter (dict[str, Any]): Filters for exact matches on track attributes. Default is None. Format of entries: (attribute_name, value)
        track_listens_lower (int | None): Lower bound for track listens count filter. Default is None.
        track_listens_upper (int | None): Upper bound for track listens count filter. Default is None.
        client (QdrantClient): The QdrantClient instance to use. Default is the global client instance.
        collection_name (str): The name of the Qdrant collection to query. Default is the global collection name.

    Returns:
        tuple[list[Record], int | None]: A tuple containing a list of records (tracks) and the index of the track on the next page.
    """

    must_clauses = generate_must_clauses(exact_match_filter)

    if not (track_listens_lower is None and track_listens_upper is None):
        must_clauses.append(
            models.FieldCondition(
                key=TrackFields.TRACK_LISTENS.value,
                range=models.Range(
                    gte=float(track_listens_lower) if track_listens_lower else None,
                    lte=float(track_listens_upper) if track_listens_upper else None,
                ),
            )
        )

    return cast(
        tuple[list[Record], int | None],
        client.scroll(
            collection_name=collection_name,
            offset=offset,
            limit=limit,
            scroll_filter=models.Filter(must=must_clauses),  # type: ignore
            with_payload=True,
            with_vectors=False,
        ),
    )


def get_track_by_id(
    track_id: int,
    with_payload: bool = True,
    with_vectors: bool = False,
    client: QdrantClient = client,
    collection_name: str = COLLECTION_NAME,
) -> Record | None:
    """
    Retrieve a track by its ID.

    Args:
        track_id (int): The unique identifier of the track.
        with_payload (bool): Whether to include payload in the response. Default is True.
        with_vectors (bool): Whether to include vectors in the response. Default is False.
        client (QdrantClient): The QdrantClient instance to use. Default is the global client instance.
        collection_name (str): The name of the Qdrant collection to query. Default is the global collection name.


    Returns:
        Record | None: The retrieved track as a Record object, or None if the track doesn't exist.
    """

    tracks: list[Record] = client.retrieve(
        collection_name=collection_name,
        ids=[track_id],
        with_payload=with_payload,
        with_vectors=with_vectors,
    )
    # the DB would not allow duplicate indexes
    if len(tracks) == 1:
        return tracks[0]
    elif len(tracks) == 0:
        raise DatabaseError(f"Track with id: {track_id} does not exist.")
    else:
        raise DatabaseError("Multiple tracks with the same ID found.")


def get_most_similar_tracks(
    track_id: int | None = None,
    track_embedding: list[float] | None = None,
    limit: int = 10,
    exact_search: bool = False,
    with_payload: bool = True,
    with_vectors: bool = False,
    exact_match_filter: dict[str, Any] | None = None,
    client: QdrantClient = client,
    collection_name: str = COLLECTION_NAME,
) -> list[ScoredPoint]:
    """
    Retrieve a list of the most similar tracks to the given input, either by track ID or track embedding.

    Args:
        track_id (int | None): The ID of the track for which to find similar tracks. Set to None if using track_embedding.
        track_embedding (list[float] | None): The embedding vector of the track for which to find similar tracks.
            Set to None if using track_id.
        limit (int): The maximum number of similar tracks to retrieve. Default is 10.
        exact_search (bool): Whether to perform an exact search or not. Default is False.
        with_payload (bool): Whether to include payload data in the results. Default is True.
        with_vectors (bool): Whether to include vector data in the results. Default is False.
        exact_match_filter (dict[str, Any] | None): A dictionary specifying exact match filters for query clauses.
            Set to None if no exact match filters are needed.
        client (QdrantClient): The QdrantClient instance to use. Default is the global client instance.
        collection_name (str): The name of the Qdrant collection to query. Default is the global collection name.


    Returns:
        list[ScoredPoint]: A list of ScoredPoint objects representing the most similar tracks found.

    Raises:
        InvalidAttributeCombination: If both track_id and track_embedding are provided or if neither is provided.
        DatabaseError: If a track with the provided track_id does not exist in the database.
    """

    if track_id is None and track_embedding is None:
        raise InvalidAttributeCombination(
            "Exactly One of  `track_id` or `track_embedding` has to be non-None"
        )

    if track_id is not None and track_embedding is not None:
        raise InvalidAttributeCombination(
            "Only one of `track_id` or `track_embedding` can be non-None"
        )

    if track_id is not None:
        query_track = get_track_by_id(
            client=client,
            collection_name=collection_name,
            track_id=track_id,
            with_payload=False,
            with_vectors=True,
        )  # noqa: E501

        if query_track is None:
            raise DatabaseError(f"Track with id: {track_id} does not exist.")

        track_embedding = cast(list[float], query_track.vector)

    must_clauses = generate_must_clauses(exact_match_filter)

    return client.search(
        collection_name=collection_name,
        query_vector=track_embedding,  # type: ignore
        query_filter=models.Filter(must=must_clauses),  # type: ignore
        search_params=models.SearchParams(exact=exact_search),
        limit=limit,
        with_vectors=with_vectors,
        with_payload=with_payload,
    )


def get_tracks_full_text_match(
    match_string: str,
    offset: int,
    limit: int,
    enum_field: TrackFields,
    client: QdrantClient = client,
    collection_name: str = COLLECTION_NAME,
) -> tuple[list[Record], int | None]:
    """
    Retrieve tracks with full-text matching for a specific field.

    Args:
        match_string (str): The string to match against the specified field.
        offset (int): The starting index for pagination.
        limit (int): The maximum number of tracks to retrieve.
        enum_field (TrackFields): An enumeration representing the field to match against.
        client (QdrantClient): The QdrantClient instance to use. Default is the global client instance.
        collection_name (str): The name of the Qdrant collection to query. Default is the global collection name.

    Returns:
        tuple[list[Record], int | None]: A tuple containing a list of records (tracks) and the index of the track on the next page.
    """

    return cast(
        tuple[list[Record], int | None],
        client.scroll(
            collection_name=collection_name,
            offset=offset,
            limit=limit,
            with_payload=True,
            with_vectors=False,
            scroll_filter=models.Filter(
                must=[
                    models.FieldCondition(
                        key=enum_field.value,
                        match=models.MatchText(text=match_string),
                    )
                ]
            ),
        ),
    )


def get_number_of_datapoints(
    client: QdrantClient = client, collection_name: str = COLLECTION_NAME
) -> int:
    """
    Get the total number of data points in the specified collection.

    Args:
        client (QdrantClient): The QdrantClient instance to use. Default is the global client instance.
        collection_name (str): The name of the Qdrant collection. Default is the global collection name.

    Returns:
        int: The total number of data points in the collection.
    """

    return client.get_collection(collection_name=collection_name).points_count
