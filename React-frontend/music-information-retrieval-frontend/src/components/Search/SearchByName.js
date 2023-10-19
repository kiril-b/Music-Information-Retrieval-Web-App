import React, { useState, useEffect } from 'react';

function SearchByName() {
    const [artistName, setArtistName] = useState('');
    const [tracks, setTracks] = useState([]);
    const apiUrl = 'http://localhost:8000/tracks-library/get_tracks/artist-name';

    useEffect(() => {
        // Make the API request when the component mounts
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
                <input
                type="text"
                className="p-2 border rounded-lg"
                placeholder="Enter artist name"
                value={artistName}
                onChange={handleInputChange}
            />
            <ul>
                {tracks.map((track) => (
                     <li
                  key={track.db_id}
                  className="bg-white p-4 my-2 rounded-md shadow-md flex justify-between"
                  style={{width: '44rem'}}
                >
                  {track.track_title} - {track.artist_name}
                </li>
                ))}
            </ul>
        </div>
    );
}
export default SearchByName;