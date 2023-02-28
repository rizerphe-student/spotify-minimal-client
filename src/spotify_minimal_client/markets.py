"""All spotify markets"""
from typing import TYPE_CHECKING, Generator

if TYPE_CHECKING:
    from .client import Client


class Markets:
    """All spotify markets"""

    def __init__(self, client: "Client"):
        self.client = client

    def as_list(self) -> list[str]:
        """Get a list of all markets

        Returns:
            dict: The list of markets
        """
        return self.client.get("markets").json()

    def __iter__(self) -> Generator[str, None, None]:
        yield from self.as_list()

    def __getitem__(self, item: int) -> str:
        return self.as_list()[item]
