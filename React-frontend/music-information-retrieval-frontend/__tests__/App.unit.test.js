import React from 'react';
import { render } from '@testing-library/react';
import '@testing-library/jest-dom/extend-expect';
import App from '../src/components/App/App';

describe('App Component - unit tests', () => {
  test('should render Home button', () => {
    const { getByText } = render(<App />);
    expect(getByText('Home')).toBeInTheDocument();
  });

  test('should render Enrich Playlist button', () => {
    const { getByText } = render(<App />);
    expect(getByText('Enrich Playlist')).toBeInTheDocument();
  });

  test('should not show the library search', () => {
    const { container } = render(<App />);

    const searchLibraryComponent = container.querySelector('.showLibrarySearch');
    expect(searchLibraryComponent).not.toBeInTheDocument();
  });

  test('should not show the search by name', () => {
    const { container } = render(<App />);

    const searchLibraryComponent = container.querySelector('.showSearchByName');
    expect(searchLibraryComponent).not.toBeInTheDocument();
    
  });

  test('should not show the search by name', () => {
    const { container } = render(<App />);

    const searchLibraryComponent = container.querySelector('.showSearchByName');
    expect(searchLibraryComponent).not.toBeInTheDocument();
    
  });
  test('should not show the search by title', () => {
    const { container } = render(<App />);

    const searchLibraryComponent = container.querySelector('.showSearchByTitle');
    expect(searchLibraryComponent).not.toBeInTheDocument();
    
  });

  test('should not show playlist modal', () => {
    const { container } = render(<App />);

    const searchLibraryComponent = container.querySelector('.openPlaylistModal');
    expect(searchLibraryComponent).not.toBeInTheDocument();
    
  });

  test('should not show upload song form', () => {
    const { container } = render(<App />);

    const searchLibraryComponent = container.querySelector('.showUploadSongForm');
    expect(searchLibraryComponent).not.toBeInTheDocument();
    
  });
  
});
