import React, { useState, useEffect } from 'react';

function SearchByTitle() {
    const [title, setTitle] = useState('');
    const [tracks, setTracks] = useState([]);
    const apiUrl = 'http://localhost:8000/tracks-library/get_tracks/track-title';

    useEffect(() => {
        fetchData(title);
    }, [title]);

    const fetchData = (title) => {
        if (title) {
            const fullUrl = `${apiUrl}?track_title=${title}&offset=0`;

            fetch(fullUrl)
                .then((response) => response.json())
                .then((data) => {
                    setTracks(data);
                })
                .catch((error) => {
                    console.error('Error fetching data:', error);
                });
        }
    };

    const handleInputChange = (e) => {
        setTitle(e.target.value);
    };

    return (
        <div className='p-4'>
            <div className='grid'>
            <label className='text-white' style={{fontSize: '25px', fontWeight: '800'}} for='title-input'>Enter title</label>
            <input
                id='title-input'
                type="text"
                className="p-2 border rounded-lg text-white"
                style={{ background: 'linear-gradient(to bottom, #ff5cad, #9647ff)', width: '25rem' }}
                value={title}
                onChange={handleInputChange}
            />
            </div>

            <ul>
                {tracks.map((track) => (
                    <li
                        data-testid={track.db_id}
                        key={track.db_id}
                        className="bg-white p-4 my-2 rounded-md shadow-md flex justify-between"
                        style={{ width: '44rem' }}
                    >
                        {track.track_title} - {track.artist_name}
                    </li>
                ))}
            </ul>
        </div>
    );
}
export default SearchByTitle;