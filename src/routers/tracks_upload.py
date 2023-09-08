from typing import Annotated
from fastapi import APIRouter, HTTPException, Query, UploadFile
from fastapi.responses import FileResponse
from src.models.models import UploadedTrack

from src.service import track_operations
from src.utils.constants import NUMBER_OF_GENRES
from src.service import track_operations

tracks_upload_router = APIRouter()


@tracks_upload_router.get("/get_audio/{track_id}")
async def get_audio(track_id: int):
    track = track_operations.get_track_by_id(track_id)

    try:
        # return FileResponse(audio_file_path, media_type='audio/mpeg')
        return FileResponse(track.track_path)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Track not found")


@tracks_upload_router.post("/upload-track")
async def upload_audio_file(
    file: UploadFile,
    top_n_genres: Annotated[int, Query(le=NUMBER_OF_GENRES)] = 5,
    top_n_similar: Annotated[int, Query(ge=0)] = 10,
) -> UploadedTrack:
    if file.content_type != "audio/mpeg":
        raise HTTPException(
            status_code=400, detail="Only audio/mpeg (MP3) files are allowed."
        )

    return await track_operations.clf_and_most_similar_tracks(
        file, top_n_genres, top_n_similar
    )
