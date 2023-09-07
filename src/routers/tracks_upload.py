from fastapi import APIRouter, HTTPException, UploadFile

from src.service import track_operations

tracks_upload_router = APIRouter()


@tracks_upload_router.post("/upload-track")
async def upload_audio_file(
    file: UploadFile, top_n_genres: int = 5, top_n_similar: int = 10
):
    if file.content_type != "audio/mpeg":
        raise HTTPException(
            status_code=400, detail="Only audio/mpeg (MP3) files are allowed."
        )

    return track_operations.clf_and_most_similar_tracks(file, top_n_genres, top_n_similar)