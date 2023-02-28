"""A very simple spotify api wrapper for python."""

import base64
from typing import TypedDict

import requests

from .exceptions import (InvalidTokenResponseError, TokenNotFoundError,
                         TokenObtainError)


class AuthOptions(TypedDict):
    """Options for authentication."""

    url: str
    headers: dict[str, str]
    data: dict[str, str]


class RequestOptions(TypedDict):
    """Options for requests."""

    url: str
    headers: dict[str, str]


class Client:
    """A client for accessing the Spotify API."""

    def __init__(self, client_id: str, client_secret: str):
        """Create a new client for accessing the Spotify API.

        Args:
            client_id: The client ID for the Spotify API.
            client_secret: The client secret for the Spotify API.
        """
        self.client_id = client_id
        self.client_secret = client_secret

        self.token = self.obtain_token()
        self.base_url = "https://api.spotify.com/v1"

    def obtain_token(self) -> str:
        """Obtain an access token from the Spotify API.

        Returns:
            The access token as a string.

        Raises:
            TokenObtainError: If the API request fails.
            TokenExtractError: If the response is not valid.
        """
        auth_str = f"{self.client_id}:{self.client_secret}"
        base64_auth_str = self.encode_base64(auth_str)
        auth_header = self.build_auth_header(base64_auth_str)
        auth_options = self.build_auth_options(auth_header)

        response = requests.post(**auth_options)
        if response.status_code == 200:
            return self.extract_token(response)
        raise TokenObtainError(response.content.decode())

    def encode_base64(self, auth_str: str) -> str:
        """Encode a string in base64.

        Args:
            auth_str: The string to encode.

        Returns:
            The encoded string.
        """
        return base64.b64encode(auth_str.encode()).decode()

    def build_auth_header(self, base64_auth_str: str) -> str:
        """Build an authorization header for the Spotify API.

        Args:
            base64_auth_str: The base64-encoded client ID and secret.

        Returns:
            The authorization header as a string.
        """
        return f"Basic {base64_auth_str}"

    def build_auth_options(self, auth_header: str) -> AuthOptions:
        """Build the options for the Spotify API request.

        Args:
            auth_header: The authorization header for the request.

        Returns:
            The request options as a TypedDict.
        """
        return {
            "url": "https://accounts.spotify.com/api/token",
            "headers": {"Authorization": auth_header},
            "data": {"grant_type": "client_credentials"},
        }

    def build_req_header(self) -> str:
        """Build the authorization header for the request.

        Returns:
            The authorization header as a string.
        """
        return f"Bearer {self.token}"

    def build_req_options(self, endpoint: str, full: bool = False) -> RequestOptions:
        """Build the options for the request.

        Args:
            endpoint: The endpoint to request.
            full: Whether the endpoint is a full URL or not.

        Returns:
            The request options as a TypedDict.
        """
        req_header = self.build_req_header()
        return {
            "url": endpoint if full else f"{self.base_url}/{endpoint}",
            "headers": {"Authorization": req_header},
        }

    def get(self, endpoint: str, full: bool = False, **kwargs) -> requests.Response:
        """Make a GET request to the Spotify API.

        Args:
            endpoint: The endpoint to request.
            full: Whether the endpoint is a full URL or not.
            **kwargs: Additional arguments to pass to requests

        Returns:
            The response from the API.
        """
        req_options = self.build_req_options(endpoint, full)
        return requests.get(**req_options, **kwargs)

    def extract_token(self, response: requests.Response) -> str:
        """Extract the access token from the Spotify API response.

        Args:
            response: The response object from the API request.

        Returns:
            The access token as a string.

        Raises:
            TokenNotFoundError: If the token is not found in the response.
            InvalidTokenResponseError: If the response is not valid.
        """
        try:
            json_data = response.json()
            access_token = json_data.get("access_token")
        except (ValueError, KeyError) as err:
            raise InvalidTokenResponseError(str(err)) from None
        else:
            if not access_token:
                raise TokenNotFoundError
            return access_token
