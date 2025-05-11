import os
import json
from pytubefix import YouTube
from pytubefix.cli import on_progress

class YouTubeDownloader:
    def __init__(self, application_path):
        self.application_path = application_path

    def download_audio(self, playlist_name, video_url, song_name=None):
        try:
            yt = YouTube(video_url, on_progress_callback=on_progress, use_po_token=True)
            song_name = song_name or yt.title
            output_path = os.path.join(self.application_path, "Music", playlist_name)
            if not os.path.exists(output_path):
                os.makedirs(output_path)
            video = yt.streams.get_audio_only()
            video.download(mp3=True, output_path=output_path, filename=f"{song_name}.mp3")
            return song_name
        except Exception as e:
            print(f"Failed to download video: {e}")
            while True:
                choice = input("Enter 'E' to go back to the menu: ").capitalize()
                if choice == 'E':
                    break
            return None

    def remove_failed_song(self, playlist_name, song_name):
        playlists_file = os.path.join(self.application_path, "Music", "Playlists.json")
        with open(playlists_file, "r") as file:
            data = json.load(file)
        playlist_data = data.get(playlist_name, {})
        for key, value in list(playlist_data.items()):
            if value == song_name:
                del playlist_data[key]
                playlist_data["song_count"] = max(0, playlist_data.get("song_count", 1) - 1)
                break
        with open(playlists_file, "w") as file:
            json.dump(data, file, indent=6)
