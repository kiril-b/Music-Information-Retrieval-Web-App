import React from 'react';
import { render, fireEvent, waitFor, screen, act } from '@testing-library/react';
import '@testing-library/jest-dom';
import SearchByName from '../src/components/Search/SearchByArtistName';

const fs = require('fs');
const tracks = JSON.parse(
    fs.readFileSync('./__tests__/response_data/get_tracks_by_artist.json', 'utf8'),
);

describe('SearchByArtistName component', () => {
    test('renders component and fetches data on input change', async () => {
        act(async () => {
            const { getByLabelText, getByTestId } = render(<SearchByName />);

            await act(async () => {
                await new Promise((resolve) => setTimeout(resolve, 0));
            });

            global.fetch = jest.fn().mockResolvedValueOnce({
                status: 200,
                json: () => Promise.resolve(tracks),
            });


            fireEvent.change(getByLabelText('Enter artist name'), { target: { value: 'AW' } });

            await waitFor(() => {
                expect(global.fetch).toHaveBeenCalledWith(
                    'http://localhost:8000/tracks-library/get_tracks/artist-name?artist_name=AW&offset=0'
                );
                expect(getByText('Food - AWOL')).toBeInTheDocument();
                expect(getByText('Electric Ave - AWOL')).toBeInTheDocument();
                expect(getByText('Street Music - AWOL')).toBeInTheDocument();
            });
        });
    });
});
