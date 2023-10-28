    import React, { useState, useEffect } from 'react';
    import Modal from '../Details/Modal';
    import SimilarTracks from '../Similar Tracks/SimilarTrack';

    function SearchLibrary() {
      const [tracks, setTracks] = useState([]);
      const [loading, setLoading] = useState(true);

      const [pagination, setPagination] = useState({
        offset: 0,
        limit: 15,
        next_page_track_id: null,
      });

      const [formData, setFormData] = useState({
        track_listens_lower_bound: 0,
        track_listens_upper_bound: 0,
        genre: '',
      });

      const [selectedTrackId, setSelectedTrackId] = useState(null);
      const [selectedTrackTitle, setSelectedTrackTitle] = useState(null);

      const [isModalOpen, setIsModalOpen] = useState(false);
      const [modalDetails, setModalDetails] = useState(null);

      const [isGetSimilarClicked, setGetSimilarClicked] = useState(false);
      const [similarTracks, setSimilarTracks] = useState(null);

      const [tracker, setTracker] = useState(false);

      const fetchData = (params) => {
        const apiUrl = 'http://localhost:8000/tracks-library/get_tracks_pagination';
        const queryParams = { ...params, limit: pagination.limit, offset: pagination.offset };

        for (const key in queryParams) {
          if (queryParams[key] === undefined || queryParams[key] === '') {
            delete queryParams[key];
          }
        }

        const queryString = Object.keys(queryParams)
          .map((key) => `${key}=${queryParams[key]}`)
          .join('&');

        fetch(`${apiUrl}?${queryString}`)
          .then((response) => response.json())
          .then((data) => {
            setTracks(data[0]);
            setPagination((prevPagination) => ({
              ...prevPagination,
              next_page_track_id: data[1],
            }));
            setLoading(false);
          })
          .catch((error) => {
            console.error('Error fetching data:', error);
            setLoading(false);
          });
      };

      const handleNextPage = () => {
        const newOffset = pagination.offset + pagination.limit;
        setPagination({ ...pagination, offset: newOffset });
      };

      const handlePrevPage = () => {
        const newOffset = pagination.offset - pagination.limit;
        if (newOffset >= 0) {
          setPagination({ ...pagination, offset: newOffset });
        }
      };

      const handleFormSubmit = (e) => {
        e.preventDefault();
        fetchData({ ...pagination, ...formData });
      };

      const handleInputChange = (e) => {
        const { name, value } = e.target;
        setFormData({ ...formData, [name]: value });
      };

      const openModal = (details) => {
        setModalDetails(details);
        setIsModalOpen(true);
      };

      const closeModal = () => {
        setIsModalOpen(false);
      };

      const handleSeeDetails = (trackId) => {
        setSelectedTrackId(trackId);
        fetch(`http://localhost:8000/tracks-library/${trackId}`)
          .then((response) => response.json())
          .then((data) => {
            openModal(data);
          })
          .catch((error) => {
            console.error('Error fetching track details:', error);
          });
      };

      const openSimilarModal = (details) => {
        setSimilarTracks(details);
        setGetSimilarClicked(true);
      };

      const closeSimilarModal = () => {
        setGetSimilarClicked(false);
      };

      const handleGetSimilarTracks = (trackId, song_title) => {
        setSelectedTrackId(trackId);
        setSelectedTrackTitle(song_title);
        fetch(`http://localhost:8000/tracks-library/similar_tracks?track_id=${trackId}&number_of_similar_tracks=5`)
          .then((response) => response.json())
          .then((data) => {
            openSimilarModal(data);
          })
          .catch((error) => {
            console.error('Error fetching similar tracks: ', error);
          });
      };

      const handleAddToLocalStorage = (trackId) => {
        const existingList = JSON.parse(localStorage.getItem('selectedTracks')) || [];
        if (!existingList.includes(trackId)) {
          existingList.push(trackId);
          localStorage.setItem('selectedTracks', JSON.stringify(existingList));
        } else {
          const updatedList = existingList.filter((id) => id !== trackId);
          localStorage.setItem('selectedTracks', JSON.stringify(updatedList));
        }
        setTracker(!tracker);
      };

      const handleRemoveFromLocalStorage = (trackId) => {
        const existingList = JSON.parse(localStorage.getItem('selectedTracks')) || [];
        const updatedList = existingList.filter((id) => id !== trackId);
        localStorage.setItem('selectedTracks', JSON.stringify(updatedList));
        setTracker(!tracker);
      };


      useEffect(() => {
        if (pagination) {
          if (pagination.offset === 0) {
            const newOffset = 0;
            fetchData({ ...pagination, offset: newOffset, ...formData });
          } else {
            fetchData(pagination, formData);
          }
        }
      }, [pagination.offset, modalDetails, similarTracks, tracker]);

      const isInLocalStorage = (trackId) => {
        const existingList = JSON.parse(localStorage.getItem('selectedTracks')) || [];
        return existingList.includes(trackId);
      }


      return (
        <div className="container mx-auto">
          <form onSubmit={handleFormSubmit} className="mb-4 w-full">
            <div className="flex items-center gap-4">
              <div className="flex items-center gap-2">
                <label htmlFor="track_listens_lower_bound" className="text-white">
                  Lower Bound:
                </label>
                <input
                  type="number"
                  id="track_listens_lower_bound"
                  name="track_listens_lower_bound"
                  value={formData.track_listens_lower_bound}
                  onChange={handleInputChange}
                  className="border rounded-md px-2 py-1 w-20"
                />
              </div>
              <div className="flex items-center gap-2">
                <label htmlFor="track_listens_upper_bound" className="text-white">
                  Upper Bound:
                </label>
                <input
                  type="number"
                  id="track_listens_upper_bound"
                  name="track_listens_upper_bound"
                  value={formData.track_listens_upper_bound}
                  onChange={handleInputChange}
                  className="border rounded-md px-2 py-1 w-20"
                />
              </div>
              <div className="flex items-center gap-2">
                <label htmlFor="genre" className="text-white">
                  Genre:
                </label>
                <select
                  id="genre"
                  name="genre"
                  value={formData.genre}
                  onChange={handleInputChange}
                  className="border rounded-md px-2 py-1"
                >
                  <option value="">---</option>
                  <option value="Blues">Blues</option>
                  <option value="Classical">Classical</option>
                  <option value="Country">Country</option>
                  <option value="Easy Listening">Easy Listening</option>
                  <option value="Electronic">Electronic</option>
                  <option value="Experimental">Experimental</option>
                  <option value="Folk">Folk</option>
                  <option value="Hip-Hop">Hip-Hop</option>
                  <option value="Instrumental">Instrumental</option>
                  <option value="International">International</option>
                  <option value="Jazz">Jazz</option>
                  <option value="Old-Time / Historic">Old-Time / Historic</option>
                  <option value="Pop">Pop</option>
                  <option value="Rock">Rock</option>
                  <option value="Soul-RnB">Soul-RnB</option>
                  <option value="Spoken">Spoken</option>
                </select>
              </div>
              <div>
                <button
                  type="submit"
                  className="bg-pink-600 hover:bg-pink-700 text-white px-4 py-2 rounded-md"
                >
                  Search
                </button>
              </div>
            </div>
          </form>

          {loading ? (
            <p className="mt-4">Loading...</p>
          ) : (
            <div className="w-full">
              <ul>
                {tracks &&
                  tracks.map((track) => (
                    <li key={track.db_id} className="bg-white p-4 my-2 rounded-md shadow-md flex justify-between">
                      <div className="flex content-center">
                        {isInLocalStorage(track.db_id) ? (
                          <button
                            onClick={() => handleRemoveFromLocalStorage(track.db_id)}
                            className="bg-purple-600 hover:bg-purple-800 text-white px-2 py-1 rounded-md justify"
                          >
                            -
                          </button>
                        ) : (
                          <button
                            onClick={() => handleAddToLocalStorage(track.db_id)}
                            className="bg-pink-600 hover:bg-pink-800 text-white px-2 py-1 rounded-md justify"
                          >
                            +
                          </button>
                        )}
                        <span className="p-2">
                          {track.track_title} - {track.artist_name}
                        </span>
                      </div>
                      <div>
                        <button
                          onClick={() => handleGetSimilarTracks(track.db_id, track.track_title)}
                          className="bg-purple-600 hover:bg-purple-700 text-white px-2 py-1 rounded-md justify-end"
                        >
                          Get Similar Tracks
                        </button>
                        <button
                          onClick={() => handleSeeDetails(track.db_id)}
                          className="bg-purple-600 hover.bg-purple-700 text-white px-2 py-1 ml-2 rounded-md"
                        >
                          See Details
                        </button>
                      </div>
                    </li>
                  ))}
              </ul>
              <div className="flex items-center">
                <button
                  onClick={handlePrevPage}
                  className="bg-pink-600 hover-bg-pink-700 text-white px-4 py-2 rounded-md"
                >
                  Previous Page
                </button>
                <button
                  onClick={handleNextPage}
                  className="bg-pink-600 hover-bg-pink-700 text-white px-4 py-2 rounded-md ms-3"
                >
                  Next Page
                </button>
              </div>
            </div>
          )}

          {isModalOpen && (
            <Modal onClose={() => closeModal()} details={modalDetails} />
          )}
          {isGetSimilarClicked && (
            <SimilarTracks onCloseSimilar={closeSimilarModal} details={similarTracks} song_title={selectedTrackTitle} trackId={selectedTrackId} />
          )}
        </div>
      );
    }

    export default SearchLibrary;
