import React from 'react';
import { render, fireEvent, waitFor, act } from '@testing-library/react';
import '@testing-library/jest-dom';
import UploadSongForm from '../src/components/UploadSong/UploadSongForm';

const fs = require('fs');
const tracks = JSON.parse(
    fs.readFileSync('./__tests__/response_data/get_result_tracks_from_upload.json', 'utf8'),
);

describe('UploadSongForm component', () => {
    test('renders a blank form', () => {
        const { getByLabelText, getByText } = render(<UploadSongForm />);

        const fileInput = getByLabelText('Upload mp3 file:');
        expect(fileInput).toBeInTheDocument();

        const topNGenresInput = getByLabelText('Top N Genres:');
        const topNSimilarInput = getByLabelText('Top N Similar:');
        expect(topNGenresInput).toBeInTheDocument();
        expect(topNSimilarInput).toBeInTheDocument();

        const uploadButton = getByText('Upload');
        expect(uploadButton).toBeInTheDocument();
    });

    test('uploads a song with specific parameters', async () => {
        act(async () => {

            const { getByLabelText, getByTestId } = render(<UploadSongForm />);

            await act(async () => {
                await new Promise((resolve) => setTimeout(resolve, 0));
            });

            const fileInput = getByLabelText('Upload mp3 file:');
            fireEvent.change(fileInput, { target: { files: [new File([''], 'FastAPI-backend\src\audio\ViVii - Wrap Your Arms (128 kbps).mp3')] } });

            const topNGenresInput = getByLabelText('Top N Genres:');
            const topNSimilarInput = getByLabelText('Top N Similar:');
            fireEvent.change(topNGenresInput, { target: { value: '3' } });
            fireEvent.change(topNSimilarInput, { target: { value: '4' } });


            global.fetch = jest.fn().mockResolvedValueOnce({
                status: 200,
                json: () => Promise.resolve(tracks),
            });

            const uploadButton = getByText('Upload');
            fireEvent.click(uploadButton);

            await waitFor(() => {
                expect(global.fetch).toHaveBeenCalledTimes(1);


                expect(getByText('Genre Prediction')).toBeInTheDocument();
                expect(getByText('Electronic: 43%')).toBeInTheDocument();
                expect(getByText('Pop: 31%')).toBeInTheDocument();
                expect(getByText('Experimental: 10%')).toBeInTheDocument();

                expect(getByTestId('Most Similar Tracks')).toBeInTheDocument();

                expect(getByText('3 am West End')).toBeInTheDocument();
                expect(getByText('Join the Bahamas')).toBeInTheDocument();
                expect(getByText('Another Time (rehearsal take)')).toBeInTheDocument();
                expect(getByText('Forest Friends')).toBeInTheDocument();

            });
        });
    });
});
