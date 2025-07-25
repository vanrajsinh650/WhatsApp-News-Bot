import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from dotenv import load_dotenv, find_dotenv
from pathlib import Path
from datetime import datetime
from whatsapp.message import send_message
import schedule
import time
import requests
import json


load_dotenv()

YOUTUBE_KEY = os.getenv("YOUTUBE_API")

playlist_file = os.path.join(os.path.dirname(__file__), "playlist.json")
seen_videos_file = os.path.join(os.path.dirname(__file__), "seen_videos.json")
channels_file = os.path.join(os.path.dirname(__file__), "channels.json")

video_queue = []


def load_playlist():
    try:
        with open(playlist_file, "r") as f:
            data = json.load(f)
            return data.get("playlists", {})
    except Exception as e:
        print("Error: loading playlist", e)
        return []


def fetch_playlist_from_channels():
    playlists = load_playlist()

    try:
        with open(channels_file, "r") as f:
            data = json.load(f)
            channels = data.get("channels", {})
    except Exception as e:
        print("Error loading channels.json:", e)
        return

    updated = False

    for topic, channel_id in channels.items():
        url = "https://www.googleapis.com/youtube/v3/playlists"
        params = {
            "part": "snippet",
            "channelId": channel_id,
            "maxResults": 50,
            "key": YOUTUBE_KEY,
        }

        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            items = response.json().get("items", [])
            
            new_ids = [item["id"] for item in items]
            old_ids = playlists.get(topic, [])
            combined_ids = list(set(old_ids + new_ids))

            if set(combined_ids) != set(old_ids):
                playlists[topic] = combined_ids
                print(f"Updated playlists for {topic} ({len(combined_ids)} total)")
                updated = True
            else:
                print(f"No new playlists for {topic}")

        except Exception as e:
            print(f"Error fetching playlists for {topic}: {e}")

    if updated:
        try:
            with open(playlist_file, "w") as f:
                json.dump({"playlists": playlists}, f, indent=2)
            print("Saved updated playlists to playlist.json")
        except Exception as e:
            print("Error saving playlist.json:", e)
    else:
        print("No changes to playlist.json")


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


def check_for_updates():
    global video_queue
    print("\nRunning at:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    fetch_playlist_from_channels()
    playlists = load_playlist()
    new = new_video(playlists)

    if new:
        print("NEW VIDEOS FOUND:")
        video_queue.extend(new)
        for video in new:
            print(f"[{video['topic']}] {video['title']} → {video['url']}")
        else:
            print("No new videos.")
        
def send_next_video_from_queue():
    global video_queue
    
    if video_queue:
        video = video_queue.pop(0)
        msg = f"new video in {video['topic']}!\n {video['title']}\n {video['url']}"
        send_message(msg)
    


# every 10 minutes
fetch_playlist_from_channels()
schedule.every(1).minutes.do(check_for_updates)
schedule.every(1).minutes.do(send_next_video_from_queue)

print("YouTube Video Watcher Started...\n")

while True:
    schedule.run_pending()
    time.sleep(1)
