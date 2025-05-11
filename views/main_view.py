class MainView:
    def display_menu(self):
        print("Welcome to the YouTube MP3 Playlist Application")
        print("1. Download Playlist")
        print("2. Exit")
        choice = input("Please select an option: ")
        return choice

    def show_message(self, message):
        print(message)

    def display_download_success(self, playlist_name):
        print(f"Successfully downloaded the playlist: {playlist_name}")

    def display_error(self, error_message):
        print(f"Error: {error_message}")