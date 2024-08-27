import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from duckduckgo_search import DDGS

def search_playlists_for_song(song_name):
    """
    Performs a DuckDuckGo search to find playlists containing the given song.
    :param song_name: The name of the song to search for.
    :return: List of Spotify playlist URLs.
    """
    query = f"site:open.spotify.com/playlist/ {song_name}"
    playlist_urls = []
    retry_count = 5
    backoff_factor = 2
    delay_between_requests = 2  # Add a delay between requests

    with DDGS() as ddgs:
        for attempt in range(retry_count):
            try:
                results = ddgs.text(query, max_results=10)
                if results:
                    for result in results:
                        url = result['href']
                        if 'open.spotify.com/playlist/' in url:
                            playlist_urls.append(url)
                    if playlist_urls:
                        break  # Break out of retry loop if successful
            except Exception as e:
                print(f"Error during DuckDuckGo search for '{song_name}': {e}. Retrying ({attempt + 1}/{retry_count})...")
                time.sleep(backoff_factor * (2 ** attempt) + delay_between_requests)

    if not playlist_urls:
        print(f"No playlists found for the song: {song_name}")

    return playlist_urls

def parallel_search_playlists(song_names):
    """
    Performs DuckDuckGo searches in parallel to find playlists containing the given songs.
    :param song_names: List of song names to search for.
    :return: Dictionary mapping song names to lists of Spotify playlist URLs.
    """
    max_workers = 3  # Reduce the number of concurrent threads

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_song = {executor.submit(search_playlists_for_song, song_name): song_name for song_name in song_names}
        results = {}
        
        for future in as_completed(future_to_song):
            song_name = future_to_song[future]
            try:
                results[song_name] = future.result()
            except Exception as e:
                print(f"Error during DuckDuckGo search for song '{song_name}': {e}")
        
    return results
