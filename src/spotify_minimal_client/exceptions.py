"""A collection of errors that might arise when using the Spotify API."""


class SpotifyAPIError(Exception):
    """Base class for Spotify API errors."""


class TokenObtainError(SpotifyAPIError):
    """Exception raised when an error occurs while obtaining an access token."""

    def __init__(self, message: str):
        super().__init__(f"Failed to obtain access token: {message}")


class TokenExtractError(SpotifyAPIError):
    """Exception raised when an error occurs while extracting an access token."""

    def __init__(self, message: str):
        super().__init__(f"Failed to extract access token: {message}")


class TokenNotFoundError(TokenExtractError):
    """Exception raised when the access token is not found in the response."""

    def __init__(self) -> None:
        super().__init__("Token not found in response")


class InvalidTokenResponseError(TokenExtractError):
    """Exception raised when the response is not a valid JSON object."""

    def __init__(self, message: str):
        super().__init__(f"Invalid response: {message}")


class ClientNotInjectedError(SpotifyAPIError):
    """Exception raised when the client is not injected into an object."""

    def __init__(self) -> None:
        super().__init__("Client not injected into object")


class NoNextPageError(SpotifyAPIError):
    """Exception raised when there is no next page."""

    def __init__(self) -> None:
        super().__init__("No next page")
