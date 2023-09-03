from fastapi import APIRouter, HTTPException, UploadFile
from fastapi.responses import JSONResponse
from src.service import feature_extraction

tracks_upload_router = APIRouter()

@tracks_upload_router.post('/upload-track')
async def upload_audio_file(file: UploadFile):
    if file.content_type != "audio/mpeg":
        raise HTTPException(status_code=400, detail="Only audio/mpeg (MP3) files are allowed.")
    
    await feature_extraction.extract_features(file)
    
    return JSONResponse(content={"message": "Files uploaded successfully"})