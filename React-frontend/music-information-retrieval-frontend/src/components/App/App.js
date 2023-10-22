import React, { useState } from 'react';
import SearchLibrary from '../SearchLibrary/SearchLibrary';
import MusicNoteIcon from './MusicNoteIcon';
import './App.css';
import SearchByName from '../Search/SearchByArtistName';
import SearchByTitle from '../Search/SearchByTitle';
import LocalTrackModal from '../Playlist/Playlist';
import TrackUpload from '../UploadSong/UploadSongForm';
import UploadSongForm from '../UploadSong/UploadSongForm';

function App() {
  const [showLibrarySearch, setShowLibrarySearch] = useState(false);
  const [showSearchByName, setShowSearchByName] = useState(false);
  const [showSearchByTitle, setShowSearchByTitle] = useState(false);
  const [openPlaylistModal, setOpenPlaylistModal] = useState(false);
  const [showUploadSongForm, setShowUploadSongForm] = useState(false);



  const handleLibrarySearchClick = () => {
    setShowLibrarySearch(true);
    setShowSearchByName(false);
    setShowSearchByTitle(false);
    setShowUploadSongForm(false);
  };

  const handleSearchByNameClick = () => {
    setShowLibrarySearch(false);
    setShowSearchByName(true);
    setShowSearchByTitle(false);
    setShowUploadSongForm(false);
  };

  const handleSearchByTitleClick = () => {
    setShowLibrarySearch(false);
    setShowSearchByName(false);
    setShowSearchByTitle(true);
    setShowUploadSongForm(false);
  };

  const handleHomeClick = () => {
    setShowLibrarySearch(false);
    setShowSearchByName(false);
    setShowSearchByTitle(false);
    setShowUploadSongForm(false);
  };

  const handleUploadSongClick = () => {
    setShowLibrarySearch(false);
    setShowSearchByName(false);
    setShowSearchByTitle(false);
    setShowUploadSongForm(true);
  };

  const handleShowPlaylistClick = () => {
    setOpenPlaylistModal(true);
  }

  const closePlaylistModal = () => {
    setOpenPlaylistModal(false);
  }

  return (
    <div className="w-full bg-gray-900">
      <div className="w-full text-black flex">
        <div className='mt-12'>        
          <MusicNoteIcon />
        </div>
        <div style={{width: '32rem', marginLeft: '-38rem', marginTop: '11.7rem', marginRight: '9rem'}}>
          <button onClick={handleHomeClick}  className=''>
          <svg xmlns="http://www.w3.org/2000/svg" x="0px" y="0px" width="40" height="20" viewBox="0 0 50 50" fill='white'>
<path d="M 24.960938 2.1015625 A 1.0001 1.0001 0 0 0 24.386719 2.3105469 L 1.3867188 20.210938 A 1.0001 1.0001 0 1 0 2.6132812 21.789062 L 4 20.708984 L 4 48 A 1.0001 1.0001 0 0 0 5 49 L 18.832031 49 A 1.0001 1.0001 0 0 0 19.158203 49 L 30.832031 49 A 1.0001 1.0001 0 0 0 31.158203 49 L 45 49 A 1.0001 1.0001 0 0 0 46 48 L 46 20.708984 L 47.386719 21.789062 A 1.0001 1.0001 0 1 0 48.613281 20.210938 L 25.613281 2.3105469 A 1.0001 1.0001 0 0 0 24.960938 2.1015625 z M 25 4.3671875 L 44 19.154297 L 44 47 L 32 47 L 32 29 A 1.0001 1.0001 0 0 0 31 28 L 19 28 A 1.0001 1.0001 0 0 0 18 29 L 18 47 L 6 47 L 6 19.154297 L 25 4.3671875 z M 20 30 L 30 30 L 30 47 L 20 47 L 20 30 z"></path>
</svg> <span className='text-white'>Home</span>
          </button>
        </div>

        <div style={{width: '35rem', marginLeft: '-43rem', marginTop: '23.8rem', marginRight: '9rem'}}>
          <button onClick={handleShowPlaylistClick}  className='text-white'>
            My Playlist
          </button>
        </div>

        <div className="grid">
  <div className="flex">
    <button
      onClick={handleLibrarySearchClick}
      className={showLibrarySearch ? "hidden" : "btn"}
      style={{ marginRight: '1rem'}}
    >
      Search Library
    </button>
    <button
      onClick={handleSearchByNameClick}
      className={showSearchByName ? "hidden" : "btn"}
      style={{ marginRight: '1rem'}}
    >
      Search By Artist Name
    </button>
    <button
      onClick={handleSearchByTitleClick}
      className={showSearchByTitle ? "hidden" : "btn"}
      style={{ marginRight: '1rem'}}
    >
      Search By Title
    </button>
    <button
      onClick={handleUploadSongClick}
      className={showUploadSongForm ? "hidden" : "btn"}
      style={{ marginRight: '1rem'}}
    >
      Upload Song
    </button>
  </div>
  <div className="marginRight" style={{ marginRight: '4rem' }}>
    {showLibrarySearch && <SearchLibrary />}
    {showSearchByName && <SearchByName />}
    {showSearchByTitle && <SearchByTitle />}
    {openPlaylistModal && <LocalTrackModal trackIds={localStorage.getItem('selectedTracks') || []} onClose={closePlaylistModal} />}
    {showUploadSongForm && <UploadSongForm />}
  </div>
</div>

      </div>
    </div>
  );
}

export default App;
