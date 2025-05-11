import os
import json
import shutil

class PlaylistModel:
    def __init__(self, application_path):
        self.application_path = application_path
        self.playlists_file = os.path.join(self.application_path, "Music", "Playlists.json")
        self.ensure_playlists_file_exists()

    def ensure_playlists_file_exists(self):
        if not os.path.exists(self.playlists_file):
            os.makedirs(os.path.dirname(self.playlists_file), exist_ok=True)
            with open(self.playlists_file, "w") as file:
                json.dump({}, file)

    def get_playlists(self):
        with open(self.playlists_file, "r") as save_file:
            return json.load(save_file)

    def save_playlists(self, data):
        with open(self.playlists_file, "w") as save_file:
            json.dump(data, save_file, indent=6)

    def delete_playlist(self, playlist):
        data = self.get_playlists()
        data.pop(playlist, None)
        self.save_playlists(data)
        playlist_path = os.path.join(self.application_path, "Music", playlist)
        if os.path.exists(playlist_path):
            shutil.rmtree(playlist_path)

    def create_playlist(self, playlist):
        playlist_path = os.path.join(self.application_path, "Music", playlist)
        if not os.path.isdir(playlist_path):
            os.makedirs(playlist_path)
            data = self.get_playlists()
            data[playlist] = {"song_count": 0}
            self.save_playlists(data)

    def rename_playlist(self, old_name, new_name):
        data = self.get_playlists()
        if old_name in data:
            data[new_name] = data.pop(old_name)
            self.save_playlists(data)
            old_path = os.path.join(self.application_path, "Music", old_name)
            new_path = os.path.join(self.application_path, "Music", new_name)
            os.rename(old_path, new_path)

    def get_songs(self, playlist):
        data = self.get_playlists()
        return data.get(playlist, {})

    def delete_song(self, playlist, song):
        data = self.get_playlists()
        playlist_data = data.get(playlist, {})
        song_path = os.path.join(self.application_path, "Music", playlist, f"{song}.mp3")
        if os.path.isfile(song_path):
            os.remove(song_path)
        playlist_data.pop(song, None)
        playlist_data["song_count"] = max(0, playlist_data.get("song_count", 1) - 1)
        self.save_playlists(data)

    def add_song_to_playlist(self, playlist_name, song_name):
        data = self.get_playlists()
        playlist_data = data.get(playlist_name, {})
        song_count = playlist_data.get("song_count", 0) + 1
        playlist_data[f"song {song_count}"] = song_name
        playlist_data["song_count"] = song_count
        self.save_playlists(data)
