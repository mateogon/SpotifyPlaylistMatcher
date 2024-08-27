import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

load_dotenv()

class SpotipyManager:
    def __init__(self):
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=os.getenv('SPOTIPY_CLIENT_ID'),
            client_secret=os.getenv('SPOTIPY_CLIENT_SECRET'),
            redirect_uri=os.getenv('SPOTIPY_REDIRECT_URI'),
            scope="user-library-read"))

    def get_liked_songs(self):
        liked_songs = []
        results = self.sp.current_user_saved_tracks(limit=50)

        while results:
            for item in results['items']:
                track = item['track']
                liked_songs.append({'uri': track['uri'], 'name': track['name'], 'artist': track['artists'][0]['name']})

            if results['next']:
                results = self.sp.next(results)
            else:
                break

        return liked_songs

    def get_playlist_name(self, playlist_id):
        try:
            playlist = self.sp.playlist(playlist_id)
            return playlist['name']
        except spotipy.exceptions.SpotifyException as e:
            print(f"Error fetching playlist name for {playlist_id}: {e}")
            return None
