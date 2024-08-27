import json

def load_progress(filename):
    """Loads the saved progress from a JSON file."""
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"File {filename} not found.")
        return {}

def save_progress(filename, data):
    """Saves the current progress to a JSON file."""
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

def sort_playlists_by_matches(progress):
    """Sort playlists by the number of matches in descending order."""
    sorted_playlists = sorted(progress.values(), key=lambda x: x['match_count'], reverse=True)
    return sorted_playlists

def main():
    # Load the playlist progress data
    progress_data = load_progress('playlist_progress.json')
    
    if not progress_data:
        print("No progress data found.")
        return

    # Sort the playlists by the number of matches
    sorted_playlists = sort_playlists_by_matches(progress_data)
    
    # Save the sorted playlists to a new JSON file
    save_progress('sorted_playlists.json', sorted_playlists)
    
    print("Playlists sorted by match count and saved to 'sorted_playlists.json'.")

if __name__ == "__main__":
    main()
