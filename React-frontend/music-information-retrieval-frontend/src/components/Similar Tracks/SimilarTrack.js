import React from 'react';
import './ModalSimilar.css';

function SimilarTracks({ details, onCloseSimilar, song_title }) {
  return (
    <div className="modal-similar">
      <div className="modal-similar-content">
      <button className="modal-similar-close-button" onClick={onCloseSimilar}>&times;</button>
        <h2 className='text-center'>List of Similar Tracks for <span className="song_title">{song_title}</span></h2>
        <ul className="song-list">
          {details.map((item) => (
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
