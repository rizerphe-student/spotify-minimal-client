"""Spotify copyright."""
import enum

from pydantic.dataclasses import dataclass


class CopyrightType(enum.Enum):
    """The type of the copyright."""

    C = "C"
    P = "P"


@dataclass
class Copyright:
    """The copyright."""

    text: str
    type: CopyrightType
