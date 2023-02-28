"""A representation of spotify albums."""
from __future__ import annotations

import datetime
import enum
from typing import TYPE_CHECKING

from pydantic.dataclasses import dataclass

from .artist import Artist
from .copyright import Copyright
from .image import Image
from .restrictions import Restrictions
from .track import RawTracks, Tracks

if TYPE_CHECKING:
    from .client import Client


class AlbumType(enum.Enum):
    """The type of album."""

    ALBUM = "album"
    SINGLE = "single"
    COMPILATION = "compilation"


class DatePrecision(enum.Enum):
    """The precision of the date."""

    YEAR = "year"
    MONTH = "month"
    DAY = "day"


@dataclass
class ExternalIds:
    """The external ids."""

    upc: str | None = None
    ean: str | None = None
    isrc: str | None = None


@dataclass
class Album:
    """A spotify album."""

    id: str
    album_type: AlbumType
    total_tracks: int
    available_markets: tuple[str, ...]
    external_urls: dict[str, str]
    href: str
    images: tuple[Image, ...]
    name: str
    release_date: datetime.date
    release_date_precision: DatePrecision
    uri: str
    external_ids: ExternalIds
    genres: tuple[str, ...]
    label: str
    popularity: int
    artists: tuple[Artist, ...]
    raw_tracks: RawTracks
    copyrights: tuple[Copyright, ...] | None = None
    restrictions: Restrictions | None = None

    client = None

    @classmethod
    def fetch(cls, client: Client, identifier: str) -> Album:
        """Fetch an album.

        Args:
            client (Client): The client to use.
            identifier (str): The album identifier.

        Returns:
            Album: The album.
        """
        data = client.get(f"albums/{identifier}").json()

        # We replace "tracks" with "raw_tracks" to enable pagination.
        data["raw_tracks"] = data.pop("tracks")

        constructed = cls(**data)

        # Inject the client.
        constructed.client = client
        for artist in constructed.artists:
            artist.client = client

        return constructed

    @property
    def tracks(self) -> Tracks | None:
        """The tracks of the album.

        Returns:
            Tracks: The tracks.
        """
        if self.client is None:
            return None
        return Tracks(self.raw_tracks, self.client)


class Albums:
    """A representation of spotify albums."""

    def __init__(self, client: Client) -> None:
        """Initialize.

        Args:
            client (Client): The client to use.
        """
        self._client = client

    def __getitem__(self, identifier: str) -> Album:
        """Get an album.

        Args:
            identifier (str): The album identifier.

        Returns:
            Album: The album.
        """
        return Album.fetch(self._client, identifier)
