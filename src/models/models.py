from pydantic import BaseModel

class Track(BaseModel):
    db_id: int | None = None
    track_id: int
    track_path: str
    track_title: str
    artist_name: str
    track_duration: int 
    track_genre: str
    track_listens: int


class ScoredTrack(Track):
	similarity_score: float
	
	
class UploadedTrack(BaseModel):
	most_similar_tracks: list[ScoredTrack]
	genre_prediction: dict[str, float]
