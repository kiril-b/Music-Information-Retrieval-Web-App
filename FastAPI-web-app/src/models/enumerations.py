from enum import Enum


class GenreEnum(str, Enum):
    POP = "Pop"
    JAZZ = "Jazz"
    ROCK = "Rock"
    FOLK = "Folk"
    BLUES = "Blues"
    SPOKEN = "Spoken"
    HIP_HOP = "Hip-Hop"
    COUNTRY = "Country"
    SOUL_RnB = "Soul-RnB"
    CLASSICAL = "Classical"
    ELECTRONIC = "Electronic"
    EXPERIMENTAL = "Experimental"
    INSTRUMENTAL = "Instrumental"
    INTERNATIONAL = "International"
    EASY_LISTENING = "Easy Listening"
    OLD_TIME_HISTORIC = "Old-Time / Historic"


# TODO: Change these feilds to match the names of the attributes in the db
class TrackFields(str, Enum):
    DB_ID = "db_id"
    TRACK_ID = "track_id"
    GENRE = "meta_genre_top"
    TRACK_PATH = "meta_track_path"
    TRACK_TITLE = "meta_track_title"
    ARTIST_NAME = "meta_artist_name"
    TRACK_LISTENS = "meta_track_listens"
    TRACK_DURATION = "meta_track_duration"
    SIMILARITY_SCORE = "similarity_score"
