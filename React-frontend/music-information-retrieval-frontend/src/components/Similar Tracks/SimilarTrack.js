import React, { useState } from 'react';
import './ModalSimilar.css';

function SimilarTracks({ details, onCloseSimilar, song_title, trackId }) {
  const [numberOfSimilarTracks, setNumberOfSimilarTracks] = useState(10);
  const [artistName, setArtistName] = useState('');
  const [tracks, setTracks] = useState(details);

  const handleFormSubmit = (e) => {
    e.preventDefault();

    let apiUrl = `http://localhost:8000/tracks-library/similar_tracks?track_id=${trackId}`;

    if(numberOfSimilarTracks){
        apiUrl += `&number_of_similar_tracks=${numberOfSimilarTracks}`;
    }   
    if (artistName) {
      apiUrl += `&artist_name=${artistName}`;
    }


    fetch(apiUrl)
      .then((response) => response.json())
      .then((data) => {
        setTracks(data);
        console.logdata();
      })
      .catch((error) => {
        console.error('Error fetching similar tracks:', error);
      });
  };

  return (
    <div className="modal-similar">
      <div className="modal-similar-content">
        <button className="modal-similar-close-button" onClick={onCloseSimilar}>
          &times;
        </button>
        <h2 className='text-center'>
          List of Similar Tracks for <span className="song_title">{song_title}</span>
        </h2>
        <form onSubmit={handleFormSubmit} className="flex mb-4 w-full gap-3">
          <div className="form-group flex items-center gap-1">
            <label className=" text-white" htmlFor="numberOfSimilarTracks">Number of Similar Tracks:</label>
            <input
              type="number"
              id="numberOfSimilarTracks"
              name="numberOfSimilarTracks"
              value={numberOfSimilarTracks}
              onChange={(e) => setNumberOfSimilarTracks(e.target.value)}
              className="border rounded-md px-2 py-1 w-20"
            />
          </div>
          <div className="form-group flex items-center gap-1">
            <label className=" text-white" htmlFor="artistName">Artist Name:</label>
            <input
              type="text"
              id="artistName"
              name="artistName"
              value={artistName}
              onChange={(e) => setArtistName(e.target.value)}
              className="border rounded-md px-2 py-1 w-20"
            />
          </div>
          <button type="submit" className="bg-pink-600 hover:bg-pink-700 text-white px-1 py-2 rounded-md w-20 flex justify-center"
>
          <svg xmlns="http://www.w3.org/2000/svg" x="0px" y="0px" width="50" height="30" viewBox="0 0 30 30" fill='white'>
<path d="M 13 3 C 7.4889971 3 3 7.4889971 3 13 C 3 18.511003 7.4889971 23 13 23 C 15.396508 23 17.597385 22.148986 19.322266 20.736328 L 25.292969 26.707031 A 1.0001 1.0001 0 1 0 26.707031 25.292969 L 20.736328 19.322266 C 22.148986 17.597385 23 15.396508 23 13 C 23 7.4889971 18.511003 3 13 3 z M 13 5 C 17.430123 5 21 8.5698774 21 13 C 21 17.430123 17.430123 21 13 21 C 8.5698774 21 5 17.430123 5 13 C 5 8.5698774 8.5698774 5 13 5 z"></path>
</svg>
          </button>
        </form>
        <ul className="song-list">
          {tracks.map((item) => (
            <li key={item.db_id} className="song-item">
              <h3 className="song-title">{item.track_title}</h3>
              <p className="song-artist">Artist: {item.artist_name}</p>
              <p className="song-info">Genre: {item.track_genre}</p>
              <p className="song-info">Duration: {item.track_duration} seconds</p>
              <p className="song-info">Listens: {item.track_listens}</p>
              <p className="song-info">Similarity Score: {item.similarity_score}</p>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}

export default SimilarTracks;
