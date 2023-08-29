import uvicorn
from fastapi import FastAPI, Response
from src.routers.tracks_library import tracks_router

app = FastAPI()


@app.get("/ping")
def read_root():
    return Response(status_code=200, content='The application is running!')


app.include_router(tracks_router, prefix='/tracks', tags=['tracks'])

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
