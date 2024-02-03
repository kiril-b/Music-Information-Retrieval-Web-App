from qdrant_client.http.models.models import Record, ScoredPoint

from src.models.models import Track, ScoredTrack
from src.models.enumerations import TrackFields


def record_to_track(record: Record | ScoredPoint | None) -> Track | ScoredTrack:
    """
    Convert a Qdrant Record or ScoredPoint to a Track or ScoredTrack object.

    Args:
        record (Record | ScoredPoint | None): The Qdrant Record or ScoredPoint to be converted.

    Returns:
        Track | ScoredTrack: A Track or ScoredTrack object created from the provided record.

    Raises:
        ValueError: If the provided record is None or does not have payload.
        ValueError: If the object passed is not an instance of Record or ScoredPoint.
    """

    if record is None:
        raise ValueError("The provided record is None")
    elif record.payload is None:
        raise ValueError(
            'The record does not have payload. Make sure the fetching from the DB is done with "with_payload=True"'
        )

    # TODO: Use the enum for attribute names
    # The keys of this dict must match the pydantic model
    track_data = {
        "db_id": record.id,
        "track_id": record.payload[TrackFields.TRACK_ID.value],
        "track_path": "./src/audio/Kid Bloom Cowboy Official Visualizer.mp3",
        "track_title": record.payload[TrackFields.TRACK_TITLE.value],
        "artist_name": record.payload[TrackFields.ARTIST_NAME.value],
        "track_duration": record.payload[TrackFields.TRACK_DURATION.value],
        "track_genre": record.payload[TrackFields.GENRE.value],
        "track_listens": record.payload[TrackFields.TRACK_LISTENS.value],
    }

    if isinstance(record, Record):
        return Track(**track_data)
    elif isinstance(record, ScoredPoint):
        track_data["similarity_score"] = record.score
        return ScoredTrack(**track_data)
    else:
        raise ValueError(
            "Passed object should be one of: qdrant_client.http.models.models.Record, qdrant_client.http.models.models.ScoredPoint"
        )
