import uvicorn
from fastapi import FastAPI, Response
from src.routers.tracks_library import tracks_library_router
from src.routers.tracks_upload import tracks_upload_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


@app.get("/ping")
def read_root():
    return Response(status_code=200, content="The application is running!")


app.include_router(
    tracks_library_router, prefix="/tracks-library", tags=["tracks_library"]
)
app.include_router(
    tracks_upload_router, prefix="/tracks-upload", tags=["tracks_upload_router"]
)

origins = [
    "http://localhost:3000", 
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
