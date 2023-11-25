import React from 'react';
import { render, screen, fireEvent, act, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom/extend-expect';

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

    // test('should search songs by filter', () => {
    //     render(<App />);

    //     const button = screen.getByText('Search Library');

    //     act(() => {
    //         fireEvent.click(button);
    //     });
    //     expect(screen.getByText('Loading...')).toBeInTheDocument();
    // });

    
});