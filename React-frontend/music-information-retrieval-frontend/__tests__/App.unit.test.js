import React from 'react';
import { render, screen } from '@testing-library/react';
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

    const searchLibraryComponent = container.querySelector('.showLibrarySearchSelector');
    expect(searchLibraryComponent).not.toBeInTheDocument();
  });

  test('should not show the search by name', () => {
    const searchLibraryComponent = screen.queryByTestId('search-by-name-component');
    expect(searchLibraryComponent).not.toBeInTheDocument();

  });
  test('should not show the search by title', () => {
    const searchLibraryComponent = screen.queryByTestId('search-by-title-component');
    expect(searchLibraryComponent).not.toBeInTheDocument();

  });

  test('should not show playlist modal', () => {
    const searchLibraryComponent = screen.queryByTestId('playlist-modal-component');
    expect(searchLibraryComponent).not.toBeInTheDocument();

  });

  test('should not show upload song form', () => {
    const searchLibraryComponent = screen.queryByTestId('upload-song-form-component');
    expect(searchLibraryComponent).not.toBeInTheDocument();

  });
});
