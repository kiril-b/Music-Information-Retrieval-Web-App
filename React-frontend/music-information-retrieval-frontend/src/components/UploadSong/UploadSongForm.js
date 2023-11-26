import React, { useState, useEffect } from 'react';
import './UploadSong.css';

function UploadSongForm() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [topNGenres, setTopNGenres] = useState(5);
  const [topNSimilar, setTopNSimilar] = useState(10);
  const [genrePrediction, setGenrePrediction] = useState({});
  const [mostSimilarTracks, setMostSimilarTracks] = useState([]);
  const [audioSrc, setAudioSrc] = useState(null);
  const [showPlayButton, setShowPlayButton] = useState(false);
  const [indexOfPlaySong, setIndexOfPlaySong] = useState();


  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0]);
  };

  const handleUpload = async () => {
    if (!selectedFile) {
      alert('Please select an MP3 file to upload.');
      return;
    }

    const queryParams = new URLSearchParams();

    if (topNGenres) {
      queryParams.append('top_n_genres', topNGenres);
    }

    if (topNSimilar) {
      queryParams.append('top_n_similar', topNSimilar);
    }

    const apiUrl = `http://localhost:8000/tracks-upload/upload-track?${queryParams.toString()}`;

    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
      const response = await fetch(apiUrl, {
        method: 'POST',
        body: formData,
      });

      if (response.ok) {
        const data = await response.json();
        setGenrePrediction(data.genre_prediction);
        setMostSimilarTracks(data.most_similar_tracks);
      } else {
        alert('Failed to upload the song.');
      }
    } catch (error) {
      console.error('Error uploading the song:', error);
    }
  };

  const handlePlayClick = (trackIndex) => {
    if (mostSimilarTracks[trackIndex] && mostSimilarTracks[trackIndex].track_id) {
      fetch(`http://localhost:8000/tracks-upload/get_audio/${mostSimilarTracks[trackIndex].db_id}`)
        .then((response) => {
          if (response.status === 200) {
            response.blob().then((blob) => {
              const audioBlob = URL.createObjectURL(blob);
              setAudioSrc(audioBlob);
              setShowPlayButton(true);
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

  return (
    <div className="track-upload-container">
      <div className="file-input">
      <label className="text-white" for='upload'>Upload mp3 file: </label>
        <input type="file" accept=".mp3" id='upload' onChange={handleFileChange}/>
      </div>
      <div className="upload-options">
        <label className="text-white" for='n_genres'>Top N Genres: </label>
        <input type="number" value={topNGenres} id='n_genres' onChange={(e) => setTopNGenres(e.target.value)} className="input-field" />
        <label className="text-white" for='n_similar'>Top N Similar: </label>
        <input type="number" value={topNSimilar} onChange={(e) => setTopNSimilar(e.target.value)} className="input-field" />
        <button onClick={handleUpload} id='n_similar' className="upload-button">Upload</button>
      </div>
      {Object.keys(genrePrediction).length > 0 && (
        <div className="genre-prediction" style={{borderTop:' 1px solid white', borderBottom: ' 1px solid white'}}>
          <h2 className='' style={{fontSize: '28px',   color:' #5f0448', fontWeight: '800'
}}>Genre Prediction</h2>
          <ul>
            {Object.entries(genrePrediction).map(([genre, percentage]) => (
              <li key={genre} className="genre-item">
                {genre}: {Math.round(percentage)}%
              </li>
            ))}
          </ul>
        </div>
      )}
      {mostSimilarTracks.length > 0 && (
        <div className="most-similar-tracks">
          <h2 style={{fontSize: '28px',   color:' #5f0448', fontWeight: '800'
}}>Most Similar Tracks</h2>
          {mostSimilarTracks.map((track, index) => (
            <div key={track.track_id} className="track-item">
              <h3 style={{color: '#ff6b6b', fontSize: '20px'}}>{track.track_title}</h3>
              <p>Artist: {track.artist_name}</p>
              <p>Duration: {track.track_duration} seconds</p>
              <p>Genre: {track.track_genre}</p>
              <p>Similarity Score: {track.similarity_score}</p>
              { indexOfPlaySong !== index &&(
                   <div className="play-button-upload" onClick={() => handlePlayClick(index)}>
                   Play
                 </div>
              )}
           
                {audioSrc &&  showPlayButton && indexOfPlaySong === index && (
                <audio controls>
                <source src={audioSrc} type="audio/mpeg" />
                Your browser does not support the audio element.
                </audio>
            )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default UploadSongForm;
