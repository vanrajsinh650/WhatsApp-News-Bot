from dotenv import load_dotenv, find_dotenv
from pathlib import Path
import requests
import json
import os

load_dotenv()

YOUTUBE_KEY = os.getenv("YOUTUBE_API")

playlist_file = os.path.join(os.path.dirname(__file__), "playlist.json")


def load_channels():
    try:
        with open(playlist_file, "r") as f:
            data = json.load(f)
            return data.get("playlists", {})
    except Exception as e:
        print("Error: loading playlist", e)
        return []


def get_uploaded_id():
    for topic, playlist_ids in playlists.items():
        for playlist_id in playlist_ids:
            # video = get_latest_video_from_playlist(playlist_id)
            video = {"title": "Test Video Title"}  # temporary placeholder
            print(f"[{topic}] {video['title']} from {playlist_id}")


def get_latest_videos(playlists):
    url = "https://www.googleapis.com/youtube/v3/playlistItems"

    for topic, playlist_ids in playlists.items():
        for playlist_id in playlist_ids:
            params = {
                "part": "snippet",
                "playlistId": playlist_id,
                "maxResults": 1,
                "key": YOUTUBE_KEY,
            }

            try:
                response = requests.get(url, params=params)
                response.raise_for_status()
                data = response.json()

                if "items" in data and len(data["items"]) > 0:
                    item = data["items"][0]
                    title = item["snippet"]["title"]
                    video_id = item["snippet"]["resourceId"]["videoId"]
                    video_url = f"https://www.youtube.com/watch?v={video_id}"
                    print(f"[{topic}] Latest video: {title}\nURL: {video_url}\n")
                else:
                    print(f"[{topic}] No videos found in playlist {playlist_id}")

            except requests.exceptions.RequestException as e:
                print(f"[{topic}] Error fetching playlist {playlist_id}: {e}")


def load_seen_videos():
    pass


def new_video():
    pass


if __name__ == "__main__":
    playlists = load_channels()
    print("playlists:", playlists)
    get_latest_videos(playlists)
