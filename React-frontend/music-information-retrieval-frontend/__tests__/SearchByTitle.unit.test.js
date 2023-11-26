import React from 'react';
import { render, fireEvent, waitFor, screen, act } from '@testing-library/react';
import '@testing-library/jest-dom';
import SearchByTitle from '../src/components/Search/SearchByTitle';


describe('SearchByTitle component', () => {
  test('renders component and fetches data on input change', async () => {
    act(async () => {
      const { getByLabelText, getByTestId } = render(<SearchByTitle />);

      await act(async () => {
        await new Promise((resolve) => setTimeout(resolve, 0));
      });

      const mockData = [
        [
          {
            "db_id": 29,
            "track_id": 183,
            "track_path": "./src/audio/Kid Bloom Cowboy Official Visualizer.mp3",
            "track_title": "For Kate I Wait",
            "artist_name": "Ariel Pink's Haunted Graffiti",
            "track_duration": 260,
            "track_genre": "Rock",
            "track_listens": 869
          }
        ]
      ];

      global.fetch = jest.fn().mockResolvedValueOnce({
        status: 200,
        json: () => Promise.resolve(mockData),
      });


      fireEvent.change(getByLabelText('Enter title'), { target: { value: 'For Kate' } });

      await waitFor(() => {
        expect(global.fetch).toHaveBeenCalledWith(
          'http://localhost:8000/tracks-library/get_tracks/track-title?track_title=For Kate&offset=0'
        );
        expect(getByTestId('183')).toBeInTheDocument();
        expect(getByText('For Kate I Wait - Ariel Pink\'s Haunted Graffiti')).toBeInTheDocument();
      });
    });
  });
});
