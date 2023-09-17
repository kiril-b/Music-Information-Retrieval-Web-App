import React, { useState } from 'react';
import './Modal.css';

function Modal({ details, onClose }) {
    const [audioSrc, setAudioSrc] = useState(null);
    const [showPlayButton, setShowPlayButton] = useState(true);

    const handlePlayClick = () => {
        if (details && details.track_id) {
            fetch(`http://localhost:8000/tracks-upload/get_audio/${details.track_id}`)
                .then((response) => {
                    if (response.status === 200) {
                        response.blob().then((blob) => {
                            const audioBlob = URL.createObjectURL(blob);
                            setAudioSrc(audioBlob);
                            setShowPlayButton(false);
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
        <div className="modal-background">
            <div className="modal">
                <button className="modal-close" onClick={onClose}>&times;</button>
                {details ? (
                    <div className='flex justify-between'>
                        <div>
                            <div className='text-center'>
                                <h2 style={{ color: 'white', fontSize: '2rem' }}>
                                    <span style={{ color: 'pink' }}>{details.track_title}</span>
                                </h2>
                            </div>
                            <br />
                            <p style={{ color: 'white' }}>Artist: {details.artist_name}</p>
                            <p style={{ color: 'white' }}>Duration: {details.track_duration} seconds</p>
                            <p style={{ color: 'white' }}>Genre: {details.track_genre}</p>
                            <p style={{ color: 'white' }}>Listens: {details.track_listens}</p>


                        </div>
                        <div className=' mt-16 me-5'> {showPlayButton && (
                            <button
                                className="play-button"
                                onClick={handlePlayClick}
                            >
                                <svg className="w-20 h-20 text-gray-800 dark:text-white" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 10 16">
                                    <path stroke="purple" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="m2.707 14.293 5.586-5.586a1 1 0 0 0 0-1.414L2.707 1.707A1 1 0 0 0 1 2.414v11.172a1 1 0 0 0 1.707.707Z" />
                                </svg>
                            </button>
                        )}
                            {audioSrc && (
                                <audio controls>
                                    <source src={audioSrc} type="audio/mpeg" />
                                    Your browser does not support the audio element.
                                </audio>
                            )}</div></div>
                ) : (
                    <p>Loading track details...</p>
                )}
            </div>
        </div>
    );
}

export default Modal;
