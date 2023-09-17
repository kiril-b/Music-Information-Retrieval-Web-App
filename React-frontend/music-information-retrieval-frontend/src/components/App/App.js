import React, { useState } from 'react';
import SearchLibrary from '../SearchLibrary/SearchLibrary';
import MusicNoteIcon from './MusicNoteIcon';
import './App.css';

function App() {
  const [showLibrarySearch, setShowLibrarySearch] = useState(false);

  const handleButtonClick = () => {
    setShowLibrarySearch(!showLibrarySearch);
  };

  return (
    <div className="w-full bg-gray-900">
      <div className="w-full text-black flex">
<div className='mt-12'>        <MusicNoteIcon />
</div>
        <div className="grid justify-items-end mt-8">
          <button
            onClick={handleButtonClick}
            className={showLibrarySearch ? "clicked btn" : "btn"}

          >
            Search Library
          </button>
          <div className={!showLibrarySearch ? 'hidden' : 'marginRight: 2rem'}
          style={{marginRight: '4rem'}}>
            <SearchLibrary />
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
