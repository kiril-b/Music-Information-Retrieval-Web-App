import React from 'react';
import { render, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import Modal from '../src/components/Details/Modal';

const fs = require('fs');
describe('Modal component', () => {
  test('renders modal with track details and play button', async () => {
    const details = {
      "db_id": 2,
      "track_id": 5,
      "track_path": "./src/audio/Kid Bloom Cowboy Official Visualizer.mp3",
      "track_title": "This World",
      "artist_name": "AWOL",
      "track_duration": 206,
      "track_genre": "Hip-Hop",
      "track_listens": 1151
    };
    const onClose = jest.fn();

    const { getByText, getByTestId } = render(<Modal details={details} onClose={onClose} />);

    expect(getByText('This World')).toBeInTheDocument();
    expect(getByText('Artist: AWOL')).toBeInTheDocument();
    expect(getByText('Duration: 206 seconds')).toBeInTheDocument();
    expect(getByText('Genre: Hip-Hop')).toBeInTheDocument();
    expect(getByText('Listens: 1151')).toBeInTheDocument();

    const playButton = getByTestId('play-btn');
    expect(playButton).toBeInTheDocument();
    global.fetch = jest.fn().mockResolvedValueOnce({
        status: 200,
        blob: () => {
          const mp3FileContent = fs.readFileSync('FastAPI-backend\src\audio\Kid Bloom Cowboy Official Visualizer.mp3');
      
          return Promise.resolve(new Blob([mp3FileContent], { type: 'audio/mpeg' }));
        },
      });

      fireEvent.click(playButton);

    await waitFor(() => expect(global.fetch).toHaveBeenCalledTimes(1));
  });
});
