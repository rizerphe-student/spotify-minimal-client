# Spotify API Client

This is a simple client for working with the Spotify API, created as a student project. It provides a minimal set of functionality to make it easier to interact with the Spotify API in another project.
Dependencies

  - Python 3
  - Requests
  - Pydantic

# Installation

You can install this directly with pip:
```sh
pip install git+https://github.com/rizerphe-student/spotify-minimal-client.git
```

# Usage

Import the Spotify class from the spotify_minimal_client module:

```python
from spotify_minimal_client import Spotify
```

Create an instance of the SpotifyClient class, passing in your Spotify API credentials:

```python
client_id = "your-client-id"
client_secret = "your-client-secret"
client = Spotify(client_id, client_secret)
```

You can then use the client object to call various methods on the Spotify API, such as getting information about a specific track:

```python
album_id = "your-album-id"
album = client.albums[track_id]
print(album.name)
```
