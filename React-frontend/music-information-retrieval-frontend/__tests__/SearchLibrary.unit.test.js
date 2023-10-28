import React from 'react';
import { render, screen, fireEvent, act } from '@testing-library/react';
import SearchLibrary from '../src/components/SearchLibrary/SearchLibrary';
import '@testing-library/jest-dom/extend-expect';

const fs = require('fs');
const tracks = JSON.parse(
  fs.readFileSync('./__tests__/response_data/get_tracks.json', 'utf8'),
);
const tracks_pagination = JSON.parse(
  fs.readFileSync('./__tests__/response_data/get_tracks_pagination.json', 'utf8'),
);

describe('SearchLibrary Component', () => {
  beforeEach(() => {
    global.fetch = jest.fn().mockResolvedValue({
      json: () => Promise.resolve([]),
    });

    localStorage.clear();
  });

  test('renders the component with loading state', () => {

    act(() => {
      render(<SearchLibrary />);
    });

    expect(screen.getByText('Loading...')).toBeInTheDocument();
  });

  test('renders the component with data', async () => {
    const mockData = tracks;

    global.fetch.mockResolvedValueOnce({
      json: () => Promise.resolve(mockData),
    });

    act(() => {
      render(<SearchLibrary />);
    });

    await act(async () => {
      await new Promise((resolve) => setTimeout(resolve, 0));
    });

    expect(screen.queryByText('Loading...')).toBeNull();
    expect(screen.getByText('Food - AWOL')).toBeInTheDocument();

    const getSimilarButtons = screen.getAllByText('Get Similar Tracks');
    expect(getSimilarButtons.length).toBe(15);

    const getDetailsButtons = screen.getAllByText('See Details');
    expect(getDetailsButtons.length).toBe(15);

    const plusButtons = screen.getAllByText('+');
    expect(plusButtons.length).toBe(15);

  });

  test('renders form search with its default values', async () => {
    act(() => {
      render(<SearchLibrary />);
    });

    const lowerBoundInput = screen.getByLabelText('Lower Bound:');
    const upperBoundInput = screen.getByLabelText('Upper Bound:');
    const genreSelect = screen.getByLabelText('Genre:');
    const searchButton = screen.getByText('Search');

    expect(lowerBoundInput).toBeInTheDocument();
    expect(upperBoundInput).toBeInTheDocument();
    expect(genreSelect).toBeInTheDocument();
    expect(searchButton).toBeInTheDocument();

    expect(lowerBoundInput).toHaveValue(0);
    expect(upperBoundInput).toHaveValue(0);
    expect(genreSelect).toHaveValue('');

    const genreOptions = genreSelect.querySelectorAll('option');
    expect(genreOptions.length).toBe(17);
    expect(genreOptions[0]).toHaveValue('');
    expect(genreOptions[1]).toHaveValue('Blues');

    expect(screen.getByText('Lower Bound:')).toBeInTheDocument();
    expect(screen.getByText('Upper Bound:')).toBeInTheDocument();
    expect(screen.getByText('Genre:')).toBeInTheDocument();
  })

  test('loads the next page (second page)', async () => {
    global.fetch.mockResolvedValueOnce({
      json: async () => Promise.resolve(tracks_pagination),
    });

    act(() => {
      render(<SearchLibrary />);
    });

    await act(async () => {
      await new Promise((resolve) => setTimeout(resolve, 0));
    });

    const nextPageButton = screen.getByText('Next Page');

    global.fetch.mockResolvedValueOnce({
      json: async () => Promise.resolve(tracks_pagination),
    });

    act(() => {
      fireEvent.click(nextPageButton);
    });

    const secondPageTracks = await screen.findByText('Amoebiasis - Amoebic Ensemble');

  });

  test('renders the component with loading state', () => {

    act(() => {
      render(<SearchLibrary />);
    });

    expect(screen.getByText('Loading...')).toBeInTheDocument();
  });

  test('renders the component with data', async () => {
    const mockData = tracks;

    global.fetch.mockResolvedValueOnce({
      json: () => Promise.resolve(mockData),
    });

    act(() => {
      render(<SearchLibrary />);
    });

    await act(async () => {
      await new Promise((resolve) => setTimeout(resolve, 0));
    });

    expect(screen.queryByText('Loading...')).toBeNull();
    expect(screen.getByText('Food - AWOL')).toBeInTheDocument();

    const getSimilarButtons = screen.getAllByText('Get Similar Tracks');
    expect(getSimilarButtons.length).toBe(15);

    const getDetailsButtons = screen.getAllByText('See Details');
    expect(getDetailsButtons.length).toBe(15);

    const plusButtons = screen.getAllByText('+');
    expect(plusButtons.length).toBe(15);

  });

  test('add first song in local storage playlist', async () => {
    const mockData = tracks;

    global.fetch.mockResolvedValueOnce({
      json: () => Promise.resolve(mockData),
    });

    act(async () => {
      const { container } = render(<SearchLibrary />);


      await act(async () => {
        await new Promise((resolve) => setTimeout(resolve, 0));
      });

      const listItems = container.querySelectorAll('li');

      expect(listItems.length).toBeGreaterThan(0);

      const firstListItem = listItems[0];

      const plusButton = firstListItem.getByText('+');
      if (plusButton) {
        plusButton.click();
      }

      const selectedTracks = JSON.parse(localStorage.getItem('selectedTracks')) || [];
      const trackId = 0;
      const isTrackInLocalStorage = selectedTracks.includes(trackId);

      expect(isTrackInLocalStorage).toBe(true);

    });
  })

  test('remove first song in local storage playlist', async () => {
    const mockData = tracks;

    global.fetch.mockResolvedValueOnce({
      json: () => Promise.resolve(mockData),
    });

    act(async () => {
      const { container } = render(<SearchLibrary />);


      await act(async () => {
        await new Promise((resolve) => setTimeout(resolve, 0));
      });

      const listItems = container.querySelectorAll('li');

      expect(listItems.length).toBeGreaterThan(0);

      const firstListItem = listItems[0];

      const plusButton = firstListItem.getByText('-');
      if (plusButton) {
        plusButton.click();
      }

      const selectedTracks = JSON.parse(localStorage.getItem('selectedTracks')) || [];
      const trackId = 0;
      const isTrackInLocalStorage = selectedTracks.includes(trackId);

      expect(isTrackInLocalStorage).toBe(false);

    });
  })

});
