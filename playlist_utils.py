import time
from spotipy.exceptions import SpotifyException
import requests
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor, as_completed

def standardize_playlist_url(url):
    parsed_url = urlparse(url)
    playlist_id = parsed_url.path.split("/")[-1]
    return playlist_id

def compare_with_liked_songs(playlist_songs, liked_songs):
    liked_song_uris = {song['uri'] for song in liked_songs}
    matching_songs = set(playlist_songs) & liked_song_uris
    return len(matching_songs)

def retry_request(func, retries=5, backoff_factor=1):
    for i in range(retries):
        try:
            return func()
        except (requests.exceptions.ReadTimeout, SpotifyException) as e:
            if isinstance(e, SpotifyException) and e.http_status == 429:
                retry_after = int(e.headers.get('Retry-After', 1))
                print(f"Rate limited. Retrying after {retry_after} seconds...")
                time.sleep(retry_after)
            else:
                print(f"Request failed with error: {e}. Retrying ({i + 1}/{retries})...")
                time.sleep(backoff_factor * (2 ** i))
    print("Max retries reached. Skipping request.")
    return None

def get_songs_from_playlist(spm, playlist_id):
    try:
        songs = []
        results = retry_request(lambda: spm.sp.playlist_tracks(playlist_id))
        
        while results:
            for item in results['items']:
                track = item['track']
                if track:
                    songs.append(track['uri'])
            
            if results['next']:
                results = retry_request(lambda: spm.sp.next(results))
            else:
                break
        
        return songs
    except SpotifyException as e:
        print(f"Error fetching playlist {playlist_id}: {e}")
        return None

def get_songs_from_playlists_parallel(spm, playlist_ids):
    """
    Fetches songs from multiple playlists in parallel using Spotify API.
    :param spm: Instance of SpotipyManager to access Spotify API.
    :param playlist_ids: List of Spotify playlist IDs.
    :return: Dictionary mapping playlist IDs to lists of song URIs.
    """
    with ThreadPoolExecutor(max_workers=10) as executor:
        future_to_playlist = {executor.submit(get_songs_from_playlist, spm, playlist_id): playlist_id for playlist_id in playlist_ids}
        results = {}
        
        for future in as_completed(future_to_playlist):
            playlist_id = future_to_playlist[future]
            try:
                results[playlist_id] = future.result()
            except Exception as e:
                print(f"Error fetching songs from playlist '{playlist_id}': {e}")
        
    return results
