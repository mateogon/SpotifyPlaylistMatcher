import argparse
from spotify_manager import SpotipyManager
from search_utils import parallel_search_playlists
from playlist_utils import standardize_playlist_url, compare_with_liked_songs, get_songs_from_playlists_parallel
from progress_utils import save_progress, load_progress

def main(research=False):
    spm = SpotipyManager()

    # Load progress if available
    playlist_matches = load_progress('playlist_progress.json')
    processed_songs = load_progress('processed_songs.json')

    # Step 1: Get liked songs
    liked_songs = spm.get_liked_songs()
    print(f"Found {len(liked_songs)} liked songs.")

    # Step 2 & 3: For each liked song, search for playlists and compare songs
    for liked_song in liked_songs:
        song_uri = liked_song['uri']
        song_name = f"{liked_song['name']} {liked_song['artist']}"

        if not research and song_uri in processed_songs:
            print(f"Skipping already processed song: {song_name}")
            continue

        print(f"Processing song: {song_name}")
        playlist_urls = parallel_search_playlists([song_name])

        if playlist_urls[song_name]:  # Only proceed if we found playlists
            playlist_ids = [standardize_playlist_url(url) for url in playlist_urls[song_name]]
            playlist_songs_map = get_songs_from_playlists_parallel(spm, playlist_ids)
                
            for playlist_id, playlist_songs in playlist_songs_map.items():
                if playlist_id in playlist_matches:
                    continue  # Skip if already processed

                match_count = compare_with_liked_songs(playlist_songs, liked_songs)
                playlist_name = spm.get_playlist_name(playlist_id)
                playlist_matches[playlist_id] = {
                    'url': f"https://open.spotify.com/playlist/{playlist_id}",
                    'name': playlist_name,
                    'match_count': match_count
                }

                # Save progress after each playlist
                save_progress('playlist_progress.json', playlist_matches)

            # Mark the song as processed only after successful processing
            processed_songs[song_uri] = song_name
            save_progress('processed_songs.json', processed_songs)

    # Step 4: Rank playlists by the number of matching liked songs
    ranked_playlists = sorted(playlist_matches.values(), key=lambda x: x['match_count'], reverse=True)

    # Save final results
    save_progress('ranked_playlists.json', ranked_playlists)

    print("\nPlaylists ranked by the number of liked songs:")
    for playlist in ranked_playlists:
        print(f"{playlist['name']} ({playlist['url']}) - {playlist['match_count']} matching liked songs")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Search and rank Spotify playlists based on liked songs.')
    parser.add_argument('--research', action='store_true', help='Re-search already processed songs.')
    args = parser.parse_args()
    
    main(research=args.research)
