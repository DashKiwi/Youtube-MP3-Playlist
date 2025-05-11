import os
import json
import time
import simpleaudio
from pydub import AudioSegment, playback

class PlayerModel:
    def __init__(self, application_path):
        self.application_path = application_path
        self.playing = False
        self.pause = False
        self.shuffling = False
        self.current_song_path = None
        self.current_timestamp = 0
        self.playback_state = "Stopped"

    def ensure_settings_file_exists(self):
        settings_file = os.path.join(self.application_path, "Settings.json")
        if not os.path.exists(settings_file):
            with open(settings_file, "w") as file:
                json.dump({"shuffling": False}, file)

    def load_settings(self):
        self.ensure_settings_file_exists()
        with open(os.path.join(self.application_path, "Settings.json"), "r") as save_file:
            return json.load(save_file)

    def save_settings(self, data):
        with open(os.path.join(self.application_path, "Settings.json"), "w") as save_file:
            json.dump(data, save_file, indent=6)

    def toggle_pause(self):
        self.pause = not self.pause

    def play_song(self, song_path):
        self.current_song_path = AudioSegment.from_file(song_path)
        self.current_timestamp = 0
        self.playback_state = "Playing"
        self.playing = True
        self._play_audio()

    def _play_audio(self):
        if self.current_song_path:
            raw_data = self.current_song_path.raw_data
            music = simpleaudio.play_buffer(
                raw_data,
                num_channels=self.current_song_path.channels,
                bytes_per_sample=self.current_song_path.sample_width,
                sample_rate=self.current_song_path.frame_rate
            )
            return music

    def stop_audio(self):
        simpleaudio.stop_all()
        self.playing = False
        self.playback_state = "Stopped"
