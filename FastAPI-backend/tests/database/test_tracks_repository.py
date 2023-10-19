import os
import pytest
from dotenv import load_dotenv
from qdrant_client import QdrantClient, models

from src.repository import tracks_repository
from src.models.enumerations import TrackFields
from src.models.exceptions.exceptions import InvalidAttributeCombination
from src.utils.repo_utils import populate_db_test
from src.models.exceptions.exceptions import DatabaseError

load_dotenv()
TEST_COLLECTION_NAME = "test-collection"


@pytest.fixture(scope="function")
def qdrant_client():
    client = QdrantClient(url=os.getenv("QDRANT_URL"))
    client.recreate_collection(
        collection_name=TEST_COLLECTION_NAME,
        vectors_config=models.VectorParams(size=3, distance=models.Distance.EUCLID),
    )
    return client


def test_tracks_retrieval__given_limit__returns_tracks(qdrant_client):
    # given
    vectors = [[0, 0, 0], [1, 1, 1], [3, 3, 3]]
    populate_db_test(
        qdrant_client=qdrant_client,
        collection_name=TEST_COLLECTION_NAME,
        vectors=vectors,
    )

    # when
    limit = 1
    tracks, _ = tracks_repository.get_tracks(
        client=qdrant_client, collection_name=TEST_COLLECTION_NAME, limit=limit
    )

    # then
    assert (
        len(tracks) == limit
    ), """
    The number of tracks retrieved should be 2"""


def test_search_tracks__given_exact_match__returns_filtered_tracks(qdrant_client):
    # given
    vectors = [[0, 0, 0], [1, 1, 1], [3, 3, 3]]
    payloads = [{"atr": 1}, {"atr": 2}, {"atr": 1}]
    populate_db_test(
        qdrant_client=qdrant_client,
        collection_name=TEST_COLLECTION_NAME,
        vectors=vectors,
        payloads=payloads,
    )

    # when
    tracks, _ = tracks_repository.get_tracks(
        client=qdrant_client,
        collection_name=TEST_COLLECTION_NAME,
        exact_match_filter={"atr": 1},
    )

    # then
    assert all(
        track.payload["atr"] == 1 for track in tracks
    ), """
    Fetched tracks include attribute values that are not supposed to be present."""


def test_search_track__given_listens_thresholds__returns_filtered_tracks(qdrant_client):
    # given
    vectors = [[0, 0, 0], [1, 1, 1], [3, 3, 3]]
    payloads = [{"track_listens": 1}, {"track_listens": 2}, {"track_listens": 3}]
    populate_db_test(
        qdrant_client=qdrant_client,
        collection_name=TEST_COLLECTION_NAME,
        vectors=vectors,
        payloads=payloads,
    )

    # when
    LOWER_BOUND, UPPER_BOUND = 1, 5
    tracks, _ = tracks_repository.get_tracks(
        client=qdrant_client,
        collection_name=TEST_COLLECTION_NAME,
        track_listens_lower=LOWER_BOUND,
        track_listens_upper=UPPER_BOUND,
    )

    # then
    assert all(
        LOWER_BOUND < track.payload["track_listens"] < UPPER_BOUND for track in tracks
    ), "Tracks are not within the range for the track_listens attribute"


def test_search_track__given_listsns_and_exact_matches__returns_filtered_tracks(
    qdrant_client,
):
    # given
    vectors = [[0, 0, 0], [1, 1, 1], [3, 3, 3]]
    payloads = [
        {"track_listens": 1, "atr": 1},
        {"track_listens": 2, "atr": 2},
        {"track_listens": 3, "atr": 1},
    ]
    populate_db_test(
        qdrant_client=qdrant_client,
        collection_name=TEST_COLLECTION_NAME,
        vectors=vectors,
        payloads=payloads,
    )

    # when
    LOWER_BOUND, UPPER_BOUND = 1, 5
    tracks, _ = tracks_repository.get_tracks(
        client=qdrant_client,
        collection_name=TEST_COLLECTION_NAME,
        track_listens_lower=LOWER_BOUND,
        track_listens_upper=UPPER_BOUND,
        exact_match_filter={"atr": 1},
    )

    # then
    assert all(
        LOWER_BOUND <= track.payload["track_listens"] <= UPPER_BOUND
        and track.payload["atr"] == 1
        for track in tracks
    ), """
    Fetched articles include attribute values that were not specified in the filtering 
    condition or fall outside the range for the specified track listens range (or both)"""


def test_get_track__given_id__returns_appropriate_track(qdrant_client):
    # given
    vectors = [[0, 0, 0], [1, 1, 1]]
    populate_db_test(
        qdrant_client=qdrant_client,
        collection_name=TEST_COLLECTION_NAME,
        vectors=vectors,
    )

    # when
    t_id = 0
    track = tracks_repository.get_track_by_id(
        client=qdrant_client,
        collection_name=TEST_COLLECTION_NAME,
        track_id=t_id,
        with_payload=False,
        with_vectors=False,
    )

    # then
    assert track.id == t_id, """Fetched track has different id from the query"""


def test_get_track__given_invalid_id__raises_exception(qdrant_client):
    # given
    vectors = [[0, 0, 0], [1, 1, 1]]
    populate_db_test(
        qdrant_client=qdrant_client,
        collection_name=TEST_COLLECTION_NAME,
        vectors=vectors,
    )

    # when/then
    with pytest.raises(DatabaseError):
        t_id = 10
        _ = tracks_repository.get_track_by_id(
            client=qdrant_client,
            collection_name=TEST_COLLECTION_NAME,
            track_id=t_id,
            with_payload=True,
            with_vectors=True,
        )


def test_get_similar_tracks__given_id_and_embedding__raises_exception(qdrant_client):
    # given
    vectors = [[0, 0, 0], [1, 1, 1]]
    populate_db_test(
        qdrant_client=qdrant_client,
        collection_name=TEST_COLLECTION_NAME,
        vectors=vectors,
    )

    # when/then
    with pytest.raises(InvalidAttributeCombination):
        track_id = 0
        track_embedding = [3.0, 3.0, 3.0]
        tracks_repository.get_most_similar_tracks(
            client=qdrant_client,
            collection_name=TEST_COLLECTION_NAME,
            track_id=track_id,
            track_embedding=track_embedding,
        )


def test_get_similar_tracks__not_given_id_nor_embedding__raises_exception(qdrant_client):
    # given
    vectors = [[0, 0, 0], [1, 1, 1]]
    populate_db_test(
        qdrant_client=qdrant_client,
        collection_name=TEST_COLLECTION_NAME,
        vectors=vectors,
    )

    # when/then
    with pytest.raises(InvalidAttributeCombination):
        track_id = None
        track_embedding = None
        tracks_repository.get_most_similar_tracks(
            client=qdrant_client,
            collection_name=TEST_COLLECTION_NAME,
            track_id=track_id,
            track_embedding=track_embedding,
        )


def test_get_exact_track_by_similarity__given_id__returns_same_track(qdrant_client):
    # given
    vectors = [[0, 0, 0], [1, 1, 1]]
    populate_db_test(
        qdrant_client=qdrant_client,
        collection_name=TEST_COLLECTION_NAME,
        vectors=vectors,
    )

    # when
    t_id = 0
    tracks = tracks_repository.get_most_similar_tracks(
        client=qdrant_client,
        collection_name=TEST_COLLECTION_NAME,
        track_id=t_id,
        exact_search=True,
        limit=1,
    )

    # then
    assert (
        tracks[0].id == t_id
    ), """There exists a track that is more similar to the original track, than the original track itself"""


def test_get_similar_tracks__given_embedding_and_exact_matches__returns_appropriate_similar_tracks(
    qdrant_client,
):
    # given
    vectors = [[0, 0, 0], [1, 1, 1], [2, 2, 2]]
    payloads = [{"atr": 1}, {"atr": 2}, {"atr": 1}]
    populate_db_test(
        qdrant_client=qdrant_client,
        collection_name=TEST_COLLECTION_NAME,
        vectors=vectors,
        payloads=payloads,
    )

    # when
    track_embedding = [3.0, 3.0, 3.0]
    tracks = tracks_repository.get_most_similar_tracks(
        client=qdrant_client,
        collection_name=TEST_COLLECTION_NAME,
        track_embedding=track_embedding,
        exact_match_filter={"atr": 1},
        limit=5,
        with_payload=True,
        with_vectors=True,
    )
    closest_track = min(tracks, key=lambda t: t.score)

    # then
    assert all(
        track.payload["atr"] == 1 for track in tracks
    ) and closest_track.vector == [
        2.0,
        2.0,
        2.0,
    ], """
    Returned tracks are not within the subsets specified by the exact match filters"""


def test_get_tracks__given_substring__returns_filtered_tracks(qdrant_client):
    # given
    vectors = [[0, 0, 0], [1, 1, 1]]
    payloads = [
        {TrackFields.ARTIST_NAME.value: "lana del rey"},
        {TrackFields.ARTIST_NAME.value: "lana"},
        {TrackFields.ARTIST_NAME.value: "frank ocean"},
    ]
    populate_db_test(
        qdrant_client=qdrant_client,
        collection_name=TEST_COLLECTION_NAME,
        vectors=vectors,
        payloads=payloads,
    )

    # when
    tracks, _ = tracks_repository.get_tracks_full_text_match(
        match_string="lana",
        offset=0,
        limit=10,
        enum_field=TrackFields.ARTIST_NAME,
        client=qdrant_client,
        collection_name=TEST_COLLECTION_NAME,
    )

    # then
    assert all(
        "lana" in track.payload[TrackFields.ARTIST_NAME.value] for track in tracks
    )


def test_get_number_of_tracks__given_collection__returns_number_of_tracks(
    qdrant_client,
):
    # given
    vectors = [[0, 0, 0], [1, 1, 1]]
    populate_db_test(
        qdrant_client=qdrant_client,
        collection_name=TEST_COLLECTION_NAME,
        vectors=vectors,
    )

    # when
    num_tracks = tracks_repository.get_number_of_datapoints(
        client=qdrant_client, collection_name=TEST_COLLECTION_NAME
    )

    assert num_tracks == 2
