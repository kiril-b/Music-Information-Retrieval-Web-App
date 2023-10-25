import React from 'react';
import { render, screen, fireEvent, act, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom/extend-expect';
import App from '../src/components/App/App';

const fs = require('fs');
const tracks = JSON.parse(
    fs.readFileSync('./__tests__/response_data/get_tracks_pagination.json', 'utf8'),
);

global.fetch = jest.fn((url) => {
    if (url === 'http://localhost:8000/tracks-library/get_tracks_pagination?offset=0&limit=15&next_page_track_id=null&track_listens_lower_bound=0&track_listens_upper_bound=0') {
        return Promise.resolve({
            json: () => Promise.resolve(tracks),
        });
    }
});

describe('App Component - integration tests', () => {

    test('should start load search library data after button click', () => {
        render(<App />);

        const button = screen.getByText('Search Library');

        act(() => {
            fireEvent.click(button);
        });
        expect(screen.getByText('Loading...')).toBeInTheDocument();
    });

    test('should load Search By Artist Name component on button click', async () => {

        render(<App />);

        const button = screen.getByText('Search By Artist Name');

        expect(button).toBeInTheDocument();

        act(() => {
            fireEvent.click(button);
        });

        await waitFor(() => {
            expect(screen.getByText('Enter artist name')).toBeInTheDocument();
        });
    });

    test('should load Search By Title component on button click', async () => {

        render(<App />);

        const button = screen.getByText('Search By Title');

        expect(button).toBeInTheDocument();

        act(() => {
            fireEvent.click(button);
        });

        await waitFor(() => {
            expect(screen.getByText('Enter title')).toBeInTheDocument();
        });
    });

    test('should render Enrich Playlist component on button click', async () => {

        render(<App />);

        const button = screen.getByText('Enrich Playlist');
        fireEvent.click(button);
      
        const modalTitle = screen.getByText('Enrich Playlist'); 
        expect(modalTitle).toBeInTheDocument();
    });

    test('should render Upload song component on button click', async () => {

        render(<App />);

        const button = screen.getByText('Upload Song');
        fireEvent.click(button);
      
        await waitFor(() => {
            expect(screen.getByText('Upload mp3 file:')).toBeInTheDocument();
        });
    });
});