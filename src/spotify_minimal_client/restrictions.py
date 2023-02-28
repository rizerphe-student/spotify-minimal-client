"""The spotify restrictions."""
import enum

from pydantic.dataclasses import dataclass


class RestrictionReason(enum.Enum):
    """The reason for the restriction."""

    MARKET = "market"
    PRODUCT = "product"
    EXPLICIT = "explicit"


@dataclass
class Restrictions:
    """The restrictions."""

    reason: RestrictionReason
