"""A spotify track."""
from __future__ import annotations

from typing import TYPE_CHECKING, Generator

from pydantic.dataclasses import dataclass

from .artist import Artist
from .exceptions import NoNextPageError
from .restrictions import Restrictions

if TYPE_CHECKING:
    from .client import Client


@dataclass
class ExternalUrls:
    """The external urls."""

    spotify: str


@dataclass
class LinkedFrom:
    """The linked from."""

    external_urls: ExternalUrls
    href: str
    id: str
    uri: str


@dataclass
class Track:
    """A spotify track."""

    artists: tuple[Artist, ...]
    disc_number: int
    duration_ms: int
    explicit: bool
    external_urls: ExternalUrls
    href: str
    id: str
    name: str
    preview_url: str | None
    track_number: int
    uri: str
    is_local: bool
    available_markets: tuple[str, ...] = ()
    restrictions: Restrictions | None = None
    is_playable: bool | None = None
    linked_from: LinkedFrom | None = None


@dataclass
class RawTracks:
    """A raw list of spotify tracks."""

    href: str
    limit: int
    next: str | None
    offset: int
    previous: str | None
    total: int
    items: tuple[Track, ...]

    def get_next(self, client: Client) -> RawTracks:
        """Get the next page of tracks.

        Args:
            client: The client to use for accessing the Spotify API.

        Returns:
            The next page of tracks.
        """
        if self.next is None:
            raise NoNextPageError()
        data = client.get(f"{self.next}", full=True).json()
        return RawTracks(**data)


class Tracks:
    """A list of spotify tracks."""

    def __init__(self, raw_tracks: RawTracks, client: Client):
        """Initialize the tracks.

        Args:
            raw_tracks: The raw tracks.
            client: The client to use for accessing the Spotify API.
        """
        self._raw_tracks = raw_tracks
        self.client = client

    @property
    def next(self) -> Tracks | None:
        """Get the next page of tracks.

        Returns:
            The next page of tracks.
        """
        if self._raw_tracks.next is None:
            return None
        return Tracks(self._raw_tracks.get_next(self.client), self.client)

    def __iter__(self) -> Generator[Track, None, None]:
        """Iterate over the tracks.

        Yields:
            The next track.
        """
        yield from self._raw_tracks.items
        if self._raw_tracks.next is not None:
            next_tracks = self.next
            if next_tracks is not None:
                yield from next_tracks

    def __len__(self) -> int:
        """Get the number of tracks.

        Returns:
            The number of tracks.
        """
        return self._raw_tracks.total

    def __getitem__(self, index: int) -> Track:
        """Get a track.

        Args:
            index: The index of the track.

        Raises:
            IndexError: If the index is out of range.

        Returns:
            The track.
        """
        if index >= len(self):
            raise IndexError()
        if index < len(self._raw_tracks.items):
            track = self._raw_tracks.items[index]
            # Inject client into artists
            for artist in track.artists:
                artist.client = self.client
            return track
        next_tracks = self.next
        if next_tracks is None:
            raise IndexError()
        return next_tracks[index - len(self._raw_tracks.items)]
