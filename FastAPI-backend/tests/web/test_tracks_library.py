import json
from fastapi.testclient import TestClient
import pytest
from src.main import app
from src.models.models import Track, ScoredTrack
from src.models.enumerations import GenreEnum
from src.repository import tracks_repository

client = TestClient(app)


@pytest.fixture
def track_json_keys():
    return set(Track.__annotations__.keys())


@pytest.fixture
def scored_track_json_keys():
    return set(ScoredTrack.__annotations__.keys())


@pytest.fixture
def valid_genres():
    return set(member.value for member in GenreEnum)


def test_ping():
    response = client.get("/ping")
    assert response.status_code == 200


@pytest.mark.parametrize(
    "endpoint, attribute, attribute_value, offset, limit",
    [
        ("track-title", "track_title", "life", 0, 5),
        ("track-title", "track_title", "!@#$", 0, 5),
        ("track-title", "track_title", "life", 0, None),
        ("track-title", "track_title", "life", -1, 5),
        ("track-title", "track_title", "life", 0, -1),
        ("track-title", "track_title", "life", -1, -1),
        ("artist-name", "artist_name", "AWOL", 0, 5),
        ("artist-name", "artist_name", "!@#$", 0, 5),
        ("artist-name", "artist_name", "AWOL", 0, None),
        ("artist-name", "artist_name", "AWOL", -1, 5),
        ("artist-name", "artist_name", "AWOL", 0, -1),
        ("artist-name", "artist_name", "AWOL", -1, -1),
    ],
)
def test_get_tracks_by_title_and_author_name(
    endpoint, attribute, attribute_value, offset, limit, track_json_keys
):
    q_params = {attribute: attribute_value, "offset": offset, "limit": limit}
    response = client.get(url=f"/tracks-library/get_tracks/{endpoint}", params=q_params)

    if offset >= 0 and limit and limit > 0:
        assert response.status_code == 200, """Response status code should be 200"""
        tracks_list = response.json()

        assert all(
            key in t.keys() for t in tracks_list for key in track_json_keys
        ), """Necessary keys not present in the response"""

        if limit is not None:
            assert len(tracks_list) <= limit, """More than `limit` tracks returned"""

        assert all(
            attribute_value in track[attribute] for track in tracks_list
        ), """Tracks not filtered appropriately"""
    else:
        assert response.status_code == 422, """Validation error not detected"""


@pytest.mark.parametrize(
    "offset, limit, track_listens_lower_bound, track_listens_upper_bound, genre",
    [
        (None, None, None, None, None),
        (0, 5, None, None, None),
        (0, 5, None, None, None),
        (-1, 5, None, None, None),
        (0, 0, None, None, None),
        (0, -1, None, None, None),
        (0, 5, 1000, None, None),
        (0, 5, None, 1000, None),
        (0, 5, -1, None, None),
        (0, 5, None, -1, None),
        (0, 5, None, None, "invalid_genre"),
        (0, 5, 1000, 2000, "Rock"),
    ],
)
def test_get_tracks_pagination(
    offset,
    limit,
    track_listens_lower_bound,
    track_listens_upper_bound,
    genre,
    valid_genres,
    track_json_keys,
):
    q_params = dict(
        offset=offset,
        limit=limit,
        track_listens_lower_bound=track_listens_lower_bound,
        track_listens_upper_bound=track_listens_upper_bound,
        genre=genre,
    )

    # to remove the `None` entries
    q_params = {k: v for k, v in q_params.items() if v is not None}

    response = client.get(url=f"/tracks-library/get_tracks_pagination", params=q_params)

    if (
        (offset is not None and offset >= 0)
        and (limit is not None and limit > 0)
        and (track_listens_lower_bound is None or track_listens_lower_bound > 0)
        and (track_listens_upper_bound is None or track_listens_upper_bound > 0)
        and (genre is None or genre in valid_genres)
    ):
        assert response.status_code == 200, """Response status code should be 200"""

        tracks_list, next_page_index = response.json()

        assert len(tracks_list) <= limit, """More than `limit` tracks returned"""

        assert all(
            key in t.keys() for t in tracks_list for key in track_json_keys
        ), """Necessary keys not present in the response"""

        if track_listens_lower_bound is not None:
            assert all(
                t["track_listens"] >= track_listens_lower_bound for t in tracks_list
            )

        if track_listens_upper_bound is not None:
            assert all(
                t["track_listens"] <= track_listens_upper_bound for t in tracks_list
            )

        if genre is not None:
            assert all(t["track_genre"] == genre for t in tracks_list)
    else:
        assert response.status_code == 422, """Validation error not detected"""


@pytest.mark.parametrize(
    "limit, next_page_flag",
    [
        (1, True),
        (
            tracks_repository.get_number_of_datapoints(
                collection_name="fma-music-data"
            ),
            False,
        ),  # noqa: E501
    ],
)
def test_get_tracks_next_page(limit, next_page_flag):
    q_params = dict(offset=0, limit=limit)

    response = client.get(url=f"/tracks-library/get_tracks_pagination", params=q_params)

    tracks_list, next_page_index = response.json()

    assert response.status_code == 200, """Response status code should be 200"""

    if next_page_flag:
        assert next_page_index is not None, """There should be a next page"""
    else:
        assert next_page_index is None, """There should not be a next page"""


@pytest.mark.parametrize(
    "track_id, number_of_similar_tracks, artist_name",
    [
        (1, 10, None),
        (1, 10, "AWOL"),
        (1, -1, None),
    ],
)
def test_get_similar_tracks(
    track_id, number_of_similar_tracks, artist_name, scored_track_json_keys
):
    q_params = dict(
        track_id=track_id,
        number_of_similar_tracks=number_of_similar_tracks,
        artist_name=artist_name,
    )

    # to remove the `None` entries
    q_params = {k: v for k, v in q_params.items() if v is not None}

    response = client.get(url="/tracks-library/similar_tracks", params=q_params)

    if number_of_similar_tracks > 0:
        assert response.status_code == 200, """Status code should be 200"""

        similar_tracks = response.json()

        assert all(
            key in t.keys() for t in similar_tracks for key in scored_track_json_keys
        ), """Necessary keys not present in the response"""

        assert (
            len(similar_tracks) == number_of_similar_tracks
        ), """Number of tracks returned does not match the specified number"""

        if artist_name:
            assert all(
                artist_name == scored_track["artist_name"]
                for scored_track in similar_tracks
            ), """Similar tracks not withing the subset of tracks from the specified artist"""
    
    else:
        assert response.status_code == 422, """Validation error not detected"""


def test_get_similar_tracks__given_wrong_id__raises_error():
    response = client.get(
        url="/tracks-library/similar_tracks", params={"track_id": 99999999999}
    )

    assert response.status_code == 404, """Track with invalid ID found"""


@pytest.mark.parametrize(
    "id_1, id_2, id_3",
    [
        (1, 2, 3),
        (99999, 1, 2),
        (-1, 1, 2)
    ],
)
def test_enrich_playlist(id_1, id_2, id_3, track_json_keys):
    track_ids = [id_1, id_2, id_3]
    response = client.post(
        url="/tracks-library/enrich_playlist",
        data=json.dumps(track_ids)
    )

    if any(id < 0 for id in track_ids):
        print(response.json())
        assert response.status_code == 400 and response.json() == {"detail": "All track IDs must be positive integers"}, """Negative ID should not be allowed"""
    elif 99999 in track_ids:
        print(response.json())
        assert response.status_code == 404, """Track with invalid ID found"""
    else:
        print(response.json())
        assert response.status_code == 200, """Status code should be 200"""
        tracks = response.json()
        assert all(
            key in t.keys() for t in tracks for key in track_json_keys
        ), """Necessary keys not present in the response"""
