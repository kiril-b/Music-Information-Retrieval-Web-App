import React, { useState, useEffect } from 'react';

function SearchByName() {
    const [artistName, setArtistName] = useState('');
    const [tracks, setTracks] = useState([]);
    const apiUrl = 'http://localhost:8000/tracks-library/get_tracks/artist-name';

    useEffect(() => {
        fetchData(artistName);
    }, [artistName]);

    const fetchData = (artistName) => {
        if (artistName) {
            const fullUrl = `${apiUrl}?artist_name=${artistName}&offset=0`;

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
        setArtistName(e.target.value);
    };

    return (
        <div className='p-4'>
            <div className='grid'>
                <label className='text-white' style={{ fontSize: '25px', fontWeight: '800' }}>Enter title</label>
                <input
                    type="text"
                    className="p-2 border rounded-lg"
                    placeholder="Enter artist name"
                    value={artistName}
                    onChange={handleInputChange}
                    style={{ background: 'linear-gradient(to bottom, #ff5cad, #9647ff)', width: '25rem' }}
                />
            </div>
            <ul>
                {tracks.map((track) => (
                    <li
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
export default SearchByName;