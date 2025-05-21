import os
import threading
from .player_controller import PlayerController
from models.playlist import PlaylistModel
from models.youtube_downloader import YouTubeDownloader

class AppController:
    def __init__(self, application_path):
        self.application_path = application_path
        self.playlist_model = PlaylistModel(application_path)
        self.player_controller = PlayerController(application_path)
        self.youtube_downloader = YouTubeDownloader(application_path)

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def main_menu(self):
        while True:
            self.clear_screen()
            playlists = self.playlist_model.get_playlists()
            self.menu_view.display_main_menu(playlists)
            choice = input("Enter your choice: ").capitalize()
            self.clear_screen()
            if choice == "C":
                playlist_name = input("Enter new playlist name: ")
                self.playlist_model.create_playlist(playlist_name)
            elif choice == "D":
                self.delete_playlist()
            elif choice == "X":
                break
            else:
                try:
                    choice = int(choice)
                    playlist_name = list(playlists.keys())[choice - 1]
                    self.playlist_menu(playlist_name)
                except (ValueError, IndexError):
                    self.menu_view.display_message("Invalid choice. Please try again.")

    def playlist_menu(self, playlist_name):
        while True:
            self.clear_screen()
            songs = self.playlist_model.get_songs(playlist_name)
            shuffling = self.player_controller.get_shuffling()
            print(f"Playlist: {playlist_name}\n")
            if len(songs) <= 1:  # Only 'song_count' exists
                print("You've got no music :( enter 'a' to add new songs from YouTube")
            else:
                song_index = 1
                for key, song in songs.items():
                    if key != "song_count":
                        print(f"{song_index}) {song}")
                        song_index += 1
            print(f"\np) Pause Song\ns) Skip Current Song\na) New Song\nd) Remove Song\nr) Rename Playlist\nt) Toggle Shuffle ({shuffling})\ne) Main Menu\n")
            choice = input("Enter your choice: ").capitalize()
            self.clear_screen()
            if choice == "P":
                self.player_controller.toggle_pause()
            elif choice == "S":
                self.player_controller.skip_song()
            elif choice == "A":
                self.add_song(playlist_name)
            elif choice == "D":
                self.delete_song(playlist_name)
            elif choice == "R":
                new_name = input("Enter new playlist name: ")
                self.playlist_model.rename_playlist(playlist_name, new_name)
            elif choice == "T":
                self.player_controller.toggle_shuffling()
            elif choice == "E":
                break
            else:
                self.menu_view.display_message("Invalid choice. Please try again.")

    def delete_playlist(self):
        playlists = self.playlist_model.get_playlists()
        self.menu_view.display_message("Which playlist would you like to delete?")
        for idx, playlist in enumerate(playlists.keys(), start=1):
            print(f"{idx}) {playlist}")
        try:
            choice = int(input("Enter the number corresponding to the playlist: "))
            playlist_name = list(playlists.keys())[choice - 1]
            self.playlist_model.delete_playlist(playlist_name)
            self.menu_view.display_message(f"Playlist '{playlist_name}' deleted successfully.")
        except (ValueError, IndexError):
            self.menu_view.display_message("Invalid choice. Please try again.")

    def delete_song(self, playlist_name):
        songs = self.playlist_model.get_songs(playlist_name)
        self.menu_view.display_message("Which song would you like to delete?")
        for idx, song in enumerate(songs.keys(), start=1):
            if song != "song_count":
                print(f"{idx}) {songs[song]}")
        try:
            choice = int(input("Enter the number corresponding to the song: "))
            song_key = list(songs.keys())[choice - 1]
            self.playlist_model.delete_song(playlist_name, songs[song_key])
            self.menu_view.display_message(f"Song '{songs[song_key]}' deleted successfully.")
        except (ValueError, IndexError):
            self.menu_view.display_message("Invalid choice. Please try again.")

    def add_song(self, playlist_name):
        video_url = input("Enter the YouTube link: ")
        song_name = input("Enter song name (leave blank for video title): ") or None
        try:
            downloaded_song = self.youtube_downloader.download_audio(playlist_name, video_url, song_name)
            if downloaded_song:  # Only add the song if the download was successful
                self.playlist_model.add_song_to_playlist(playlist_name, downloaded_song)
                self.menu_view.display_message(f"Song '{downloaded_song}' added successfully.")
        except RuntimeError as e:
            self.menu_view.display_message(str(e))
