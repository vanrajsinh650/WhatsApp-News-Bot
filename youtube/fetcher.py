from dotenv import load_dotenv, find_dotenv
from pathlib import Path
import requests
import json
import os

load_dotenv()

YOUTUBE_KEY = os.getenv("YOUTUBE_API")

playlist_file = os.path.join(os.path.dirname(__file__), "playlist.json")
seen_videos_file = os.path.join(os.path.dirname(__file__), "seen_videos.json")


def load_channels():
    try:
        with open(playlist_file, "r") as f:
            data = json.load(f)
            return data.get("playlists", {})
    except Exception as e:
        print("Error: loading playlist", e)
        return []


def fetch_latest_video_from_playlist(playlist_id):
    url = "https://www.googleapis.com/youtube/v3/playlistItems"
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
            return data["items"][0]
        return None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching playlist {playlist_id}: {e}")
        return None


def get_latest_videos(playlists):
    url = "https://www.googleapis.com/youtube/v3/playlistItems"

    for topic, playlist_ids in playlists.items():
        for playlist_id in playlist_ids:
            item = fetch_latest_video_from_playlist(playlist_id)
            if item:
                item = data["items"][0]
                title = item["snippet"]["title"]
                video_id = item["snippet"]["resourceId"]["videoId"]
                video_url = f"https://www.youtube.com/watch?v={video_id}"
                print(f"[{topic}] Latest video: {title}\nURL: {video_url}\n")
            else:
                print(f"[{topic}] No videos found in playlist {playlist_id}")


def load_seen_videos():
    if not os.path.exists(seen_videos_file):
        return []

    try:
        with open(seen_videos_file, "r") as f:
            data = json.load(f)
            return data.get("seen", [])
    except Exception as e:
        print("Error: loading seen videos", e)
        return []


def save_seen_videos(video_id):
    seen = load_seen_videos()

    if video_id not in seen:
        seen.append(video_id)

    try:
        with open(seen_videos_file, "w") as f:
            json.dump({"seen": seen}, f, indent=2)
    except Exception as e:
        print(f"Error saving seen video: {e}")


def new_video(playlists):
    seen = load_seen_videos()
    new_videos = []

    for topic, playlist_ids in playlists.items():
        for playlist_id in playlist_ids:
            item = fetch_latest_video_from_playlist(playlist_id)
            if item:
                video_id = item["snippet"]["resourceId"]["videoId"]
                if video_id not in seen:
                    title = item["snippet"]["title"]
                    video_url = f"https://www.youtube.com/watch?v={video_id}"
                    new_videos.append(
                        {
                            "topic": topic,
                            "title": title,
                            "url": video_url,
                            "id": video_id,
                        }
                    )

                    save_seen_videos(video_id)
                else:
                    print(f"[{topic}] Alredy seen: {video_id}")
            else:
                print(f"[{topic}] No video in playlist: {playlist_id}")

    return new_videos


if __name__ == "__main__":
    playlists = load_channels()
    print("Checking for new videos...\n")

    new = new_video(playlists)

    if new:
        print("NEW VIDEOS FOUND:")
        for video in new:
            print(f"[{video['topic']}] {video['title']} → {video['url']}")
    else:
        print("No new videos.")
