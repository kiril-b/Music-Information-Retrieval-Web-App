from fastapi import APIRouter, HTTPException, UploadFile

from src.service import classification_model

tracks_upload_router = APIRouter()

@tracks_upload_router.post('/upload-track')
async def upload_audio_file(file: UploadFile):
    if file.content_type != "audio/mpeg":
        raise HTTPException(
            status_code=400, 
            detail="Only audio/mpeg (MP3) files are allowed."
        )
    
    # await feature_extraction.extract_features(file)
    track_genre_distribution = await classification_model.classify_track(file)
    
    return classification_model.get_top_n_genres_present(
        track_y=track_genre_distribution, 
        top_n=5
    )


    # return JSONResponse(content={"message": "Files uploaded successfully"})