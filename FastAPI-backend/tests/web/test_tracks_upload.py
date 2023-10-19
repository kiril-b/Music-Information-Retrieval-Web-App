from fastapi.testclient import TestClient
import pytest
from src.main import app

client = TestClient(app)

@pytest.fixture
def track_path():
    return ".\\src\\audio\\Kid Bloom Cowboy Official Visualizer.mp3"

@pytest.mark.parametrize(
    "track_id",
    [
        (0),
        (-1),
        (99999)
    ],
)
def test_get_audio(track_id):
    response = client.get(url=f"/tracks-upload/get_audio/{track_id}")
    if track_id >= 0:
        if track_id == 99999:
            assert response.status_code == 404, """Track with non-existent ID returned"""
        else:
            assert response.status_code == 200, """Status code should be 200"""
            assert response.headers["content-type"] == "audio/mpeg", """Content type should be audio/mpeg"""
    else:
        assert response.status_code == 400, """Track with negative ID returned"""


def test_upload_audio_file_valid(track_path):
    # given
    TOP_N_SIMILAR = 10
    TOP_N_GENRES = 5

    # when
    with open(track_path, "rb") as audio_file:
        response = client.post(
            "/tracks-upload/upload-track",
            files={"file": ("Kid Bloom Cowboy Official Visualizer.mp3", audio_file, "audio/mpeg")},
            params={"top_n_genres": TOP_N_GENRES, "top_n_similar": TOP_N_SIMILAR},
        )

    # then
    assert response.status_code == 200
    
    response_json = response.json()
    assert "most_similar_tracks" in response_json.keys(), """Most similar tracks were not returned"""
    assert len(response_json["most_similar_tracks"]) == TOP_N_SIMILAR, """Wrong number of similar tracks returned"""

    assert "genre_prediction" in response_json.keys()
    assert len(response_json["genre_prediction"]) == TOP_N_GENRES, """Wrong number of genre predictions returned"""

def test_upload_audio_file_invalid_content_type(track_path):
    # given
    TOP_N_SIMILAR = 10
    TOP_N_GENRES = 5

    # when
    with open(track_path, "rb") as audio_file:
        response = client.post(
            "/tracks-upload/upload-track",
            files={"file": ("Kid Bloom Cowboy Official Visualizer.mp3", audio_file, "text/plain")},
            params={"top_n_genres": TOP_N_GENRES, "top_n_similar": TOP_N_SIMILAR},
        )


    assert response.status_code == 400, """Processed a file with invalid file type"""
    assert response.json() == {"detail": "Only audio/mpeg (MP3) files are allowed."}

def test_upload_audio_file_missing_file():
    # given
    TOP_N_SIMILAR = 10
    TOP_N_GENRES = 5

    # when
    response = client.post("/tracks-upload/upload-track", data={"top_n_genres": TOP_N_GENRES, "top_n_similar": TOP_N_SIMILAR})

    assert response.status_code == 422, """Processed request without a required filed"""
    assert "file" in response.json()["detail"][0]["loc"]

