class MenuView:
    @staticmethod
    def display_main_menu(playlists):
        print("_Open Music App_\n")
        for idx, playlist in enumerate(playlists, start=1):
            print(f"{idx}) {playlist}")
        print("\nc) New Playlist\nd) Delete Playlist\nX) Exit\n")

    @staticmethod
    def display_playlist_menu(playlist, songs, shuffling):
        print(f"{playlist}\n")
        for idx, song in enumerate(songs, start=1):
            print(f"{idx}) {song}")
        print(f"\np) Pause Song\ns) Skip Current Song\na) New Song\nd) Remove Song\nr) Rename Playlist\nt) Toggle Shuffle ({shuffling})\ne) Main Menu\n")

    @staticmethod
    def display_message(message):
        print(message)
