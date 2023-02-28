"""A spotify artist."""
from __future__ import annotations

import importlib
from typing import TYPE_CHECKING

from pydantic.dataclasses import dataclass

from .exceptions import ClientNotInjectedError
from .image import Image

if TYPE_CHECKING:
    from .client import Client
    from .track import Track


@dataclass
class ExternalUrls:
    """The external urls."""

    spotify: str


@dataclass
class Followers:
    """The followers."""

    href: str | None = None
    total: int | None = None


@dataclass
class Artist:
    """A spotify artist."""

    external_urls: ExternalUrls
    href: str
    id: str
    name: str
    uri: str
    followers: Followers | None = None
    popularity: int | None = None
    genres: tuple[str, ...] = ()
    images: tuple[Image, ...] = ()

    client = None

    @classmethod
    def fetch(cls, client: Client, identifier: str) -> Artist:
        """Fetch an artist.

        Args:
            client (Client): The client to use.
            identifier (str): The artist id.

        Returns:
            Artist: The artist.
        """
        data = client.get(f"artists/{identifier}").json()
        constructed = cls(**data)

        # Inject the client
        constructed.client = client

        return constructed

    def top_tracks(self, country: str = "US") -> tuple[Track, ...]:
        """Get the top tracks for the artist.

        Args:
            country (str, optional): The country. Defaults to None.

        Returns:
            tuple[Track, ...]: The top tracks.
        """
        if self.client is None:
            raise ClientNotInjectedError()

        data = self.client.get(
            f"artists/{self.id}/top-tracks", params={"country": country}
        ).json()

        return tuple(
            importlib.import_module("..track", __name__).Track(**track)
            for track in data["tracks"]
        )


class Artists:
    """A representation of spotify artists."""

    def __init__(self, client: Client):
        """Initialize.

        Args:
            client (Client): The client to use.
        """
        self.client = client

    def search(self, query: str) -> tuple[Artist, ...]:
        """Search for artists.

        Args:
            query (str): The query to search for.

        Returns:
            tuple[Artist, ...]: The artists.
        """
        data = self.client.get("search", params={"q": query, "type": "artist"}).json()
        artists = tuple(Artist(**artist) for artist in data["artists"]["items"])

        # Inject the client
        for artist in artists:
            artist.client = self.client

        return artists

    def __getitem__(self, identifier: str) -> Artist:
        """Get an artist.

        Args:
            identifier (str): The artist id.

        Returns:
            Artist: The artist.
        """
        return Artist.fetch(self.client, identifier)
