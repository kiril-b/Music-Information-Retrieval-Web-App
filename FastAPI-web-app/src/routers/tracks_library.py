from typing import Annotated
from fastapi import APIRouter, HTTPException, Query
from src.models.exceptions.exceptions import DatabaseError

from src.service import track_operations, playlist_enrichment
from src.models.models import ScoredTrack, Track
from src.models.enumerations import GenreEnum, TrackFields

tracks_library_router = APIRouter()


@tracks_library_router.get(
    "/get_tracks/track-title",
    description="Performs Full Text Match on the track title field in the db",
)
def get_tracks_by_name(
    track_title: str,
    offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int | None, Query(ge=1)] = None,
) -> list[Track]:
    return track_operations.get_tracks_by_full_text_match(
        track_title, offset, limit, TrackFields.TRACK_TITLE
    )


@tracks_library_router.get(
    "/get_tracks/artist-name",
    description="Performs Full Text Match on the track artist field in the db",
)
def get_tracks_by_artist(
    artist_name: str,
    offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int | None, Query(ge=1)] = None,
) -> list[Track]:
    return track_operations.get_tracks_by_full_text_match(
        artist_name, offset, limit, TrackFields.ARTIST_NAME
    )


@tracks_library_router.get(
    "/get_tracks_pagination",
    description="""Returns a tuple containing the list of 'limit'-number of Tracks, 
    as well as the offset of the track of the next page. (tracks, next_page_track_id)""",
)
def get_tracks_pagination(
    offset: Annotated[int, Query(ge=0)],
    limit: Annotated[int, Query(ge=1)],
    track_listens_lower_bound: Annotated[int | None, Query(ge=0)] = None,
    track_listens_upper_bound: Annotated[int | None, Query(ge=0)] = None,
    genre: GenreEnum | None = None,
) -> tuple[list[Track], int | None]:
    exact_match_filter = dict(
        [
            (TrackFields.GENRE, genre.value if genre else None),
        ]
    )

    return track_operations.get_tracks(
        offset=offset,
        limit=limit,
        track_listens_lower_bound=track_listens_lower_bound,
        track_listens_upper_bound=track_listens_upper_bound,
        exact_match_filter={
            k: v for k, v in exact_match_filter.items() if v is not None
        },
    )


@tracks_library_router.get("/similar_tracks")
def get_most_similar_tracks(
    track_id: Annotated[int, Query(ge=0)],
    number_of_similar_tracks: Annotated[int, Query(ge=1)] = 10,
    artist_name: str | None = None,
) -> list[ScoredTrack]:
    exact_match_filter = dict(
        [
            (TrackFields.ARTIST_NAME, artist_name),
        ]
    )

    try:
        return track_operations.find_n_most_similar_tracks_by_id(
            track_id=track_id,
            n=number_of_similar_tracks,
            exact_match_filter={
                k: v for k, v in exact_match_filter.items() if v is not None
            },
        )
    except DatabaseError as dbe:
        raise HTTPException(status_code=404, detail=dbe.message)


@tracks_library_router.get("/{track_id}")
def get_track_by_id(track_id: int) -> Track:
    if track_id < 0:
        raise HTTPException(status_code=400, detail="All track IDs must be positive integers")
    try:
        return track_operations.get_track_by_id(track_id=track_id)
    except DatabaseError as dbe:
        raise HTTPException(status_code=404, detail=dbe.message)


@tracks_library_router.post("/enrich_playlist")
def enrich_playlist(track_ids: list[int]) -> list[Track]:
    if any(id < 0 for id in track_ids):
        raise HTTPException(status_code=400, detail="All track IDs must be positive integers")
    
    try:
        return playlist_enrichment.enrich(track_ids)
    except DatabaseError as dbe:
        raise HTTPException(status_code=404, detail=dbe.message)
