# WhatsApp News Bot

This is a Python automation project that detects new YouTube videos from specific playlists and sends them to a WhatsApp number using Twilio.

## Features

- Automatically fetches **new videos** from YouTube playlists.
- Sends video updates to WhatsApp using Twilio API.
- Skips already sent videos using local JSON tracking (`seen_videos.json`).
- Uses `schedule` to run checks periodically.

## Project Structure

├── whatsapp/
│ └── message.py # Function to send message via WhatsApp (Twilio)

├── youtube/
│ ├── fetcher.py # Main script to fetch & filter new videos
│ ├── playlist.json # List of YouTube playlists with topic names
│ ├── seen_videos.json # Stores video IDs already sent
│ └── channels.json # (Optional) List of channel URLs (not used here)

├── .env # Stores YouTube and Twilio API credentials

├── requirement.txt # All dependencies


## Setup Instructions

1. **Clone the repo** and install dependencies:
   ```bash
   pip install -r requirement.txt

2. run the bot
   ```bash
   python youtube/fetcher.py


## Tech Stack

Python

Twilio API (WhatsApp messaging)

YouTube Data API v3

JSON for local storage

schedule for timed execution