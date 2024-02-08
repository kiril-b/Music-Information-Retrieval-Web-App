import "@testing-library/jest-dom/extend-expect";
import { act, fireEvent, render, screen } from "@testing-library/react";
import React from "react";
import SearchLibrary from "../src/components/SearchLibrary/SearchLibrary";

const fs = require("fs");
const tracks = JSON.parse(
  fs.readFileSync("./__tests__/response_data/get_tracks.json", "utf8")
);
const tracks_pagination = JSON.parse(
  fs.readFileSync(
    "./__tests__/response_data/get_tracks_pagination.json",
    "utf8"
  )
);

const track_listens_lower_upper_bound_genre = JSON.parse(
  fs.readFileSync(
    "./__tests__/response_data/get_tracks_by_searchlibrary_filter.json",
    "utf8"
  )
);

const handleFormSubmitMock = {
  handleFormSubmit() {
    track_listens_lower_upper_bound_genre;
  },
};

describe("SearchLibrary Component", () => {
  beforeEach(() => {
    global.fetch = jest.fn().mockResolvedValue({
      json: () => Promise.resolve([]),
    });

    localStorage.clear();
  });

  test("renders the component with loading state", () => {
    act(() => {
      render(<SearchLibrary />);
    });

    expect(screen.getByText("Loading...")).toBeInTheDocument();
  });

  test("renders the component with data", async () => {
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

    expect(screen.queryByText("Loading...")).toBeNull();
    expect(screen.getByText("Food - AWOL")).toBeInTheDocument();

    const getSimilarButtons = screen.getAllByText("tt Similar Tracks");
    expect(getSimilarButtons.length).toBe(15);

    const getDetailsButtons = screen.getAllByText("See Details");
    expect(getDetailsButtons.length).toBe(15);

    const plusButtons = screen.getAllByText("+");
    expect(plusButtons.length).toBe(15);
  });

  test("renders form search with its default values", async () => {
    act(() => {
      render(<SearchLibrary />);
    });

    const lowerBoundInput = screen.getByLabelText("Lower Bound:");
    const upperBoundInput = screen.getByLabelText("Upper Bound:");
    const genreSelect = screen.getByLabelText("Genre:");
    const searchButton = screen.getByText("Search");

    expect(lowerBoundInput).toBeInTheDocument();
    expect(upperBoundInput).toBeInTheDocument();
    expect(genreSelect).toBeInTheDocument();
    expect(searchButton).toBeInTheDocument();

    expect(lowerBoundInput).toHaveValue(0);
    expect(upperBoundInput).toHaveValue(0);
    expect(genreSelect).toHaveValue("");

    const genreOptions = genreSelect.querySelectorAll("option");
    expect(genreOptions.length).toBe(17);
    expect(genreOptions[0]).toHaveValue("");
    expect(genreOptions[1]).toHaveValue("Blues");

    expect(screen.getByText("Lower Bound:")).toBeInTheDocument();
    expect(screen.getByText("Upper Bound:")).toBeInTheDocument();
    expect(screen.getByText("Genre:")).toBeInTheDocument();
  });

  test("loads the next page (second page)", async () => {
    global.fetch.mockResolvedValueOnce({
      json: async () => Promise.resolve(tracks_pagination),
    });

    act(() => {
      render(<SearchLibrary />);
    });

    await act(async () => {
      await new Promise((resolve) => setTimeout(resolve, 0));
    });

    const nextPageButton = screen.getByText("Next Page");

    act(() => {
      fireEvent.click(nextPageButton);
    });

    await screen.findByText("Amoebiasis - Amoebic Ensemble");
  });

  test("add first song in local storage playlist", async () => {
    const mockData = tracks;

    global.fetch.mockResolvedValueOnce({
      json: () => Promise.resolve(mockData),
    });

    act(async () => {
      const { container } = render(<SearchLibrary />);

      await act(async () => {
        await new Promise((resolve) => setTimeout(resolve, 0));
      });

      const listItems = container.querySelectorAll("li");

      expect(listItems.length).toBeGreaterThan(0);

      const firstListItem = listItems[0];

      const plusButton = firstListItem.getByText("+");
      if (plusButton) {
        plusButton.click();
      }

      const selectedTracks =
        JSON.parse(localStorage.getItem("selectedTracks")) || [];
      const trackId = 0;
      const isTrackInLocalStorage = selectedTracks.includes(trackId);

      expect(isTrackInLocalStorage).toBe(true);
    });
  });

  test("remove first song in local storage playlist", async () => {
    const mockData = tracks;

    global.fetch.mockResolvedValueOnce({
      json: () => Promise.resolve(mockData),
    });

    act(async () => {
      const { container } = render(<SearchLibrary />);

      await act(async () => {
        await new Promise((resolve) => setTimeout(resolve, 0));
      });

      const listItems = container.querySelectorAll("li");

      expect(listItems.length).toBeGreaterThan(0);

      const firstListItem = listItems[0];

      const plusButton = firstListItem.getByText("-");
      if (plusButton) {
        plusButton.click();
      }

      const selectedTracks =
        JSON.parse(localStorage.getItem("selectedTracks")) || [];
      const trackId = 0;
      const isTrackInLocalStorage = selectedTracks.includes(trackId);

      expect(isTrackInLocalStorage).toBe(false);
    });
  });

  test("should return specific data regarding values in filter", async () => {
    const mockData = tracks;

    global.fetch.mockResolvedValueOnce({
      json: () => Promise.resolve(mockData),
    });

    act(async () => {
      const { container } = render(<SearchLibrary />);

      await act(async () => {
        await new Promise((resolve) => setTimeout(resolve, 0));
      });

      const inputElements = screen.getAllByPlaceholderText("0");
      const lowerBoundInput = inputElements[0];
      const upperBoundInput = inputElements[1];

      expect(lowerBoundInput).toBeInTheDocument();
      expect(lowerBoundInput).toHaveValue("0");

      expect(upperBoundInput).toBeInTheDocument();
      expect(upperBoundInput).toHaveValue("0");

      fireEvent.change(lowerBoundInput, { target: { value: "7" } });
      fireEvent.change(upperBoundInput, { target: { value: "240" } });

      const genereSelectElement = screen.getAllByPlaceholderText("---");
      fireEvent.change(genereSelectElement, { target: { value: "Country" } });

      const searchButton = screen.getByTestId("search-btn");
      expect(searchButton).toBeInTheDocument();

      const searchSpy = jest
        .spyOn(handleFormSubmit, "handleFormSubmit")
        .mockImplementation();

      if (fireEvent.click(searchButton).valueOf()) {
        handleFormSubmitMock.handleFormSubmit();
        expect(searchSpy).toHaveBeenCalled();
      }

      const songTitle = screen.getByText("Notturno");
      expect(songTitle).toBeInTheDocument();
    });
  });
});
