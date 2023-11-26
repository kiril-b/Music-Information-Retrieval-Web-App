import React from 'react';
import { render, fireEvent, waitFor, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import SimilarTracks from '../src/components/Similar Tracks/SimilarTrack';

const fs = require('fs');
const get_similar_tracks_search_filter = JSON.parse(
    fs.readFileSync('./__tests__/response_data/get_similar_tracks_search_filter.json', 'utf8'),
);

const handleSearchMock = {
    handleSearch() {
        get_similar_tracks_search_filter;
    },
};

describe('SimilarTracks component', () => {
    test('renders SimilarTracks component with initial details', () => {
        const details = [{
            "db_id": 5,
            "track_id": 10815,
            "track_path": "./src/audio/Kid Bloom Cowboy Official Visualizer.mp3",
            "track_title": "CYCLE",
            "artist_name": "AWOL",
            "track_duration": 151,
            "track_genre": "Hip-Hop",
            "track_listens": 1205,
            "similarity_score": 1.0000001
        },
        {
            "db_id": 11744,
            "track_id": 89632,
            "track_path": "./src/audio/Kid Bloom Cowboy Official Visualizer.mp3",
            "track_title": "Master Don",
            "artist_name": "BADLUCK",
            "track_duration": 171,
            "track_genre": "Hip-Hop",
            "track_listens": 236,
            "similarity_score": 0.64230347
        },
        ]

        const onCloseSimilar = jest.fn();
        const song_title = "This World";
        const trackId = 5;

        const { getByText, getByLabelText, getAllByText } = render(
            <SimilarTracks details={details} onCloseSimilar={onCloseSimilar} song_title={song_title} trackId={trackId} />
        );

        expect(getByText('List of Similar Tracks for')).toBeInTheDocument();
        expect(getByLabelText('Number of Similar Tracks:')).toHaveValue(10);
        expect(getByLabelText('Artist Name:')).toHaveValue('');

        expect(getByText('Artist: BADLUCK')).toBeInTheDocument();
        expect(getByText('Duration: 151 seconds')).toBeInTheDocument();
        expect(getByText('Listens: 1205')).toBeInTheDocument();
        expect(getByText('Similarity Score: 1.0000001')).toBeInTheDocument();

        expect(getByText('Artist: AWOL')).toBeInTheDocument();
        expect(getByText('Duration: 171 seconds')).toBeInTheDocument();
        expect(getByText('Listens: 236')).toBeInTheDocument();
        expect(getByText('Similarity Score: 0.64230347')).toBeInTheDocument();

    });

    test('handles form submission and fetches similar tracks', async () => {

        const details = [{
            "db_id": 5,
            "track_id": 10815,
            "track_path": "./src/audio/Kid Bloom Cowboy Official Visualizer.mp3",
            "track_title": "CYCLE",
            "artist_name": "AWOL",
            "track_duration": 151,
            "track_genre": "Hip-Hop",
            "track_listens": 1205,
            "similarity_score": 1.0000001
        },
        {
            "db_id": 11744,
            "track_id": 89632,
            "track_path": "./src/audio/Kid Bloom Cowboy Official Visualizer.mp3",
            "track_title": "Master Don",
            "artist_name": "BADLUCK",
            "track_duration": 171,
            "track_genre": "Hip-Hop",
            "track_listens": 236,
            "similarity_score": 0.64230347
        },
        ]

        const onCloseSimilar = jest.fn();
        const song_title = "This World";
        const trackId = 5;

        const { getByText, getByLabelText } = render(
            <SimilarTracks details={details} onCloseSimilar={onCloseSimilar} song_title={song_title} trackId={trackId} />
        );

        expect(getByText('List of Similar Tracks for')).toBeInTheDocument();
        expect(getByLabelText('Number of Similar Tracks:')).toHaveValue(10);
        expect(getByLabelText('Artist Name:')).toHaveValue('');

        fireEvent.change(getByLabelText('Number of Similar Tracks:'), { target: { value: '4' } })
        fireEvent.change(getByLabelText('Artist Name:'), { target: { value: 'AWOL' } })

        const searchButton = screen.getByTestId('search')
        expect(searchButton).toBeInTheDocument();

        global.fetch = jest.fn().mockResolvedValueOnce({
            status: 200,
            json: () => Promise.resolve(get_similar_tracks_search_filter),
        });

        fireEvent.submit(searchButton);

        await waitFor(() => {
            expect(global.fetch).toHaveBeenCalledTimes(1);

            expect(getByText('HipHop Junkfood')).toBeInTheDocument();
            expect(getByText('Duration: 73 seconds')).toBeInTheDocument();
            expect(getByText('Listens: 2323')).toBeInTheDocument();
            expect(getByText('Similarity Score: 0.5861523')).toBeInTheDocument();
    
            expect(getByText('Broken Language')).toBeInTheDocument();
            expect(getByText('Duration: 206 seconds')).toBeInTheDocument();
            expect(getByText('Listens: 335')).toBeInTheDocument();
            expect(getByText('Similarity Score: 0.5251834')).toBeInTheDocument();
          });

    });
});
