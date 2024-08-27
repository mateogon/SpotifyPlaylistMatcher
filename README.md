````markdown
# SpotifyPlaylistMatcher

SpotifyPlaylistMatcher is a Python-based tool that helps you find and match Spotify playlists based on your liked songs.

## Setup

1.  Clone the repository:

```bash
git clone https://github.com/mateogon/SpotifyPlaylistMatcher.git
cd SpotifyPlaylistMatcher
```
````

2.  Create and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

3.  Install the required packages:

```bash
pip install -r requeriments.txt
```

4.  Create a `.env` file in the root directory of the project:

```env
SPOTIPY_CLIENT_ID=your_spotify_client_id_here
SPOTIPY_CLIENT_SECRET=your_spotify_client_secret_here
SPOTIPY_REDIRECT_URI=http://localhost:8888/callback
```

5.  Run the script:

```bash
python main.py
```

## Notes

- Replace `your_spotify_client_id_here` and `your_spotify_client_secret_here` in the `.env` file with your actual Spotify API credentials.
- The `.env.sample` file provides an example configuration. Rename it to `.env` and fill in your credentials.

````

2. **Commit the `README.md` Changes:**

   ```bash
   git add README.md
   git commit -m "Add setup and usage instructions to README.md"
   git push origin main
   ```
````
