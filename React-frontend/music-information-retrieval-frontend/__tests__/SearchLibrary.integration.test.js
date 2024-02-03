import React from 'react';
import { render, screen, fireEvent, act } from '@testing-library/react';
import SearchLibrary from '../src/components/SearchLibrary/SearchLibrary';
import '@testing-library/jest-dom/extend-expect';
import { log } from 'console';

const fs = require('fs');
const tracks = JSON.parse(
    fs.readFileSync('./__tests__/response_data/get_tracks.json', 'utf8'),
);

global.fetch = jest.fn((url) => {
    if (url === 'http://localhost:8000/tracks-library/get_tracks_pagination?offset=0&limit=15&next_page_track_id=null&track_listens_lower_bound=0&track_listens_upper_bound=0') {
        return Promise.resolve({
            json: () => Promise.resolve(tracks),
        });
    }
});

describe('SearchLibrary Component - integration tests', () => {
    test('get details for Food - track', async () => {
        const mockData = tracks;
    
        global.fetch.mockResolvedValueOnce({
          json: () => Promise.resolve(mockData),
        });
    
        act(async () => {
          const { container } = render(<SearchLibrary />);
    
    
          await act(async () => {
            await new Promise((resolve) => setTimeout(resolve, 0));
          });
    
          const trackField = screen.getAllByText('Food')
          expect(trackField).toBeInTheDocument();    

          const detailsBtn = screen.getAllByText('See Details')
          const detailsFoodButton = detailsBtn[0];
          expect(detailsFoodButton).toBeInTheDocument();

          fireEvent.click(detailsFoodButton)

          const durationDetails = screen.getByText('Duration: 168 seconds')
          expect(durationDetails).toBeInTheDocument();

          const artistDetails = screen.getByText('Artist: AWOL')
          expect(artistDetails).toBeInTheDocument();

          const playTrackBtn = screen.getByTestId('play-btn')
          expect(playTrackBtn).toBeInTheDocument();

          const playTrackSpy = jest.spyOn(handlePlayClick, 'handlePlayClick').mockImplementation();

          if (fireEvent.click(detailsFoodButton).valueOf()) {
            playTrackMock.handlePlayClick();
            expect(playTrackSpy).toHaveBeenCalled();
          }          

        });
      });

      test('get similar tracks for Food - track', async () => {
        const mockData = tracks;
    
        global.fetch.mockResolvedValueOnce({
          json: () => Promise.resolve(mockData),
        });
    
        act(async () => {
          const { container } = render(<SearchLibrary />);
    
    
          await act(async () => {
            await new Promise((resolve) => setTimeout(resolve, 0));
          });
    
          const trackField = screen.getAllByText('Food')
          expect(trackField).toBeInTheDocument();    

          const similarBtns = screen.getAllByText('Get Similar Tracks')
          const similarFoodBtn = similarBtns[0];
          expect(similarFoodBtn).toBeInTheDocument();

          fireEvent.click(similarFoodBtn)

          const title = screen.getByText('List of Similar Tracks for Food')
          expect(title).toBeInTheDocument();     
        });
      });

});