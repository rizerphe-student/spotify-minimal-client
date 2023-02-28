"""The user-facing wrapper"""
from .album import Albums
from .artist import Artists
from .client import Client
from .markets import Markets


class Spotify:
    """A spotify API client."""

    def __init__(self, client_id: str, client_secret: str) -> None:
        """Initialize the spotify API client.

        Args:
            client_id: The client ID of your app.
            client_secret: The client secret of your app.
        """
        self.client = Client(client_id, client_secret)

    @property
    def albums(self) -> Albums:
        """All albums on spotify.

        Returns:
            A representation of all albums on spotify.
        """
        return Albums(self.client)

    @property
    def artists(self) -> Artists:
        """All artists on spotify.

        Returns:
            A representation of all artists on spotify.
        """
        return Artists(self.client)

    @property
    def markets(self) -> Markets:
        """All markets on spotify.

        Returns:
            A representation of all markets on spotify.
        """
        return Markets(self.client)
