"""A spotify image."""
from pydantic.dataclasses import dataclass


@dataclass
class Image:
    """An image."""

    height: int
    width: int
    url: str
