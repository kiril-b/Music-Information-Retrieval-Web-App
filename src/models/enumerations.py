from enum import Enum

class GenreEnum(str, Enum):
    POP = 'Pop'
    JAZZ = 'Jazz'
    ROCK = 'Rock'
    FOLK = 'Folk'
    BLUES = 'Blues'
    SPOKEN = 'Spoken'
    HIP_HOP = 'Hip-Hop'
    COUNTRY = 'Country'
    SOUL_RnB = 'Soul-RnB'
    CLASSICAL = 'Classical'
    ELECTRONIC = 'Electronic'
    EXPERIMENTAL = 'Experimental'
    INSTRUMENTAL = 'Instrumental'
    INTERNATIONAL = 'International'
    EASY_LISTENING = 'Easy Listening'
    OLD_TIME_HISTORIC = 'Old-Time / Historic'

class TrackFields(str, Enum):
    GENRE = 'meta_genre_top'
    ARTIST_NAME = 'meta_artist_name'