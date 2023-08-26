from fastapi import FastAPI, Response

app = FastAPI()


@app.get("/ping")
def read_root():
    return Response(status_code=200, content='The application is running!')
