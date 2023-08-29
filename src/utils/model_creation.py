from qdrant_client.http.models.models import Record, ScoredPoint

from src.models.models import Track, ScoredTrack

def record_to_track(record: Record | ScoredPoint) -> Track | ScoredTrack:

    """
    Convert a Qdrant Record or ScoredPoint to a Track or ScoredTrack object.

    Args:
        record (Record | ScoredPoint): The Qdrant Record or ScoredPoint to be converted.

    Returns:
        Track | ScoredTrack: A Track or ScoredTrack object created from the provided record.

    Raises:
        ValueError: If the provided record is None or does not have payload.
        ValueError: If the object passed is not an instance of Record or ScoredPoint.
    """

    if record is None:
        raise ValueError('The provided record is None')
    elif record.payload is None:
        raise ValueError('The record does not have payload. Make sure the fetching from the DB is done with "with_payload=True"')
    
    track_data = {
        'db_id': record.id,
        'track_id': record.payload['track_id'],
        'track_path': 'track path',
        'track_title': record.payload['meta_track_title'],
        'artist_name': record.payload['meta_artist_name'],
        'track_duration': record.payload['meta_track_duration'],
        'track_genre': record.payload['meta_genre_top'],
        'track_listens': record.payload['meta_track_listens']
    }
    
    if isinstance(record, Record):
        return Track(**track_data)
    elif isinstance(record, ScoredPoint):
        track_data['similarity_score'] = record.score
        return ScoredTrack(**track_data)
    else:
        raise ValueError('Passed object should be one of: qdrant_client.http.models.models.Record, qdrant_client.http.models.models.ScoredPoint')