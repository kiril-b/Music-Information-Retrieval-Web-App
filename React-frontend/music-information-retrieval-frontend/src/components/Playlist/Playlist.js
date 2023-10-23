import React, { useState, useEffect } from 'react';

function LocalTrackModal({ trackIds, onClose }) {
  const [details, setDetails] = useState([]);
  const [currentPage, setCurrentPage] = useState(1);
  const [tracksPerPage] = useState(3);
  const [audioSrc, setAudioSrc] = useState(null);
  const [showPlayButton, setShowPlayButton] = useState(true);
  const [indexOfPlaySong, setIndexOfPlaySong] = useState();
  const [showAudioSrc, setShowAudioSrc] = useState(false);

  useEffect(() => {
    const fetchEnrichedPlaylist = async () => {
      try {
        const response = await fetch('http://localhost:8000/tracks-library/enrich_playlist', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: trackIds,
        });

        if (response.ok) {
          const data = await response.json();
          setDetails(data);
        } else {
          console.error('Failed to fetch enriched playlist.');
        }
      } catch (error) {
        console.error('Error fetching enriched playlist:', error);
      }
    };

    if (trackIds.length > 0) {
      fetchEnrichedPlaylist();
    }
  }, [trackIds]);

  const handlePlayClick = (trackIndex) => {
    if (details[trackIndex] && details[trackIndex].track_id) {
      fetch(`http://localhost:8000/tracks-upload/get_audio/${details[trackIndex].db_id}`)
        .then((response) => {
          if (response.status === 200) {
            response.blob().then((blob) => {
              const audioBlob = URL.createObjectURL(blob);
              setAudioSrc(audioBlob);
              setShowAudioSrc(true);
              setIndexOfPlaySong(trackIndex);
            });
          } else {
            console.error('Failed to fetch audio.');
          }
        })
        .catch((error) => {
          console.error('Error fetching audio:', error);
        });
    }
  };

  const handlePageChange = (page) => {
    setCurrentPage(page);
    setAudioSrc(null);
  };

  const indexOfLastTrack = currentPage * tracksPerPage;
  const indexOfFirstTrack = indexOfLastTrack - tracksPerPage;
  const currentTracks = details.slice(indexOfFirstTrack, indexOfLastTrack);

  console.log(indexOfPlaySong);

  return (
    <div className="modal-background">
      <div className="modal">
        <button className="modal-close" onClick={onClose}>&times;</button>
        {details.length > 0 && (
          <div>
            <div className="track-container">
              {currentTracks.map((track, index) => (
                <div
                  key={track.track_id}
                  className="track-item flex justify-between col-11 px-14"
                  style={{ borderBottom: '1px solid', paddingBottom: '4px' }}
                >
                  <div className="">
                    <h2 style={{ color: 'white', fontSize: '2rem' }}>
                      <span style={{ color: 'pink' }}>{track.track_title}</span>
                    </h2>
                    <br />
                    <p style={{ color: 'white' }}>Artist: {track.artist_name}</p>
                    <p style={{ color: 'white' }}>Duration: {track.track_duration} seconds</p>
                    <p style={{ color: 'white' }}>Genre: {track.track_genre}</p>
                    <p style={{ color: 'white' }}>Listens: {track.track_listens}</p>
                  </div>
                  <div className="mt-20 flex justify-end">
                    {showPlayButton && indexOfPlaySong !== (indexOfFirstTrack + index) && (
                      <button className="play-button" onClick={() => handlePlayClick(indexOfFirstTrack + index)}>
                        <svg
                          className="w-20 h-20 text-gray-800 dark:text-white"
                          aria-hidden="true"
                          xmlns="http://www.w3.org/2000/svg"
                          fill="none"
                          viewBox="0 0 10 16"
                        >
                          <path
                            stroke="purple"
                            stroke-linecap="round"
                            stroke-linejoin="round"
                            stroke-width="2"
                            d="m2.707 14.293 5.586-5.586a1 1 0 0 0 0-1.414L2.707 1.707A1 1 0 0 0 1 2.414v11.172a1 1 0 0 0 1.707.707Z"
                          />
                        </svg>
                      </button>
                    )}
                    {audioSrc && indexOfPlaySong === (indexOfFirstTrack + index) && showAudioSrc &&
                      (<audio controls>
                        <source src={audioSrc} type="audio/mpeg" />
                        Your browser does not support the audio element.
                      </audio>)
                    }
                  </div>
                </div>
              ))}
            </div>
            <div className="pagination text-white">
              {details.length > tracksPerPage && (
                <ul className="flex gap-3">
                  {Array(Math.ceil(details.length / tracksPerPage))
                    .fill()
                    .map((_, i) => (
                      <li key={i} onClick={() => handlePageChange(i + 1)}>
                        <button className="btn btn-outline" style={{ fontSize: '15px' }}>
                          {i + 1}
                        </button>
                      </li>
                    ))}
                </ul>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default LocalTrackModal;
