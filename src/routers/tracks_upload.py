from typing import Annotated
from fastapi import APIRouter, HTTPException, Query, UploadFile

from src.service import track_operations
from src.utils.constants import NUMBER_OF_GENRES

tracks_upload_router = APIRouter()


@tracks_upload_router.post("/upload-track")
async def upload_audio_file(
    file: UploadFile,
    top_n_genres: Annotated[int, Query(le=NUMBER_OF_GENRES)] = 5,
    top_n_similar: Annotated[int, Query(ge=0)] = 10,
):
    if file.content_type != "audio/mpeg":
        raise HTTPException(
            status_code=400, detail="Only audio/mpeg (MP3) files are allowed."
        )

    return await track_operations.clf_and_most_similar_tracks(
        file, top_n_genres, top_n_similar
    )
