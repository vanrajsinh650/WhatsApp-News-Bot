import json
import os


playlist_file = os.path.join(os.path.dirname(__file__),"playlist.json")

def load_channels():
    try:
        with open(playlist_file, 'r') as f:
            data = json.load(f)
            return data.get("playlists", [])
    except Exception as e:
        print("Error: loading playlist", e)
        return []

def get_uploaded_id():
    for topic, playlist_ids in playlists.items():
        for playlist_id in playlist_ids:
            # video = get_latest_video_from_playlist(playlist_id)
            video = {"title": "Test Video Title"}  # temporary placeholder
            print(f"[{topic}] {video['title']} from {playlist_id}")

def get_latest_videos():
    pass

def load_seen_videos():
    pass

def new_video():
    pass


if __name__ == "__main__":
    channels = load_channels()
    print("playlists:", channels)
