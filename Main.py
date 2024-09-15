# Imports
import os, shutil
import simpleaudio
import json
import threading
import random
import time
import keyboard
from pathlib import Path 
from pytubefix import YouTube
from pytubefix.cli import on_progress
from pydub import AudioSegment, playback
# Global Variables
choice = 1
playlist = ""
song_continue = False
playing = False
shuffling = False
pause = False
# Functions

def playlist_delete_menu():
    global playlist
    os.system('cls||clear')
    while True:
        print("Which Playlist would you like to delete?\n\n")
        save_file = open(os.path.join(Path(__file__).resolve().parent, "Music", "Playlists.json"), "r")
        data = json.load(save_file)
        save_file.close()
        num = 0
        for playlists_json in data:
            num += 1
            print("{}) {}".format(num, playlists_json))
        if num == 0:
            os.system('cls||clear')
            print("You have no playlists. Create a new one in the menu below\n")
            return
        choice = input("\nEnter a number corrosponding to a playlist or type e to go back to main menu\n").capitalize()
        try:
            choice = eval(choice)
            if isinstance(choice, int):
                save_file = open(os.path.join(Path(__file__).resolve().parent, "Music", "Playlists.json"), "r")
                data = dict(json.load(save_file))
                save_file.close()
                itterations = 0
                for playlists_json in data.copy():
                    itterations += 1
                    if itterations == int(choice):
                        playlist = playlists_json
                        data.pop(playlist)
                        save_file = open(os.path.join(Path(__file__).resolve().parent, "Music", "Playlists.json"), "w")
                        json.dump(data, save_file, indent=6)
                        save_file.close()
                        if os.path.exists(os.path.join(Path(__file__).resolve().parent, "Music", f"{playlist}")):
                            shutil.rmtree(os.path.join(Path(__file__).resolve().parent, "Music", f"{playlist}"))
                        os.system('cls||clear')
                        return
                raise
        except:
            if choice == "E":
                return
            else:
                print("Please enter a valid option")

def song_delete_menu():
    global playlist
    os.system('cls||clear')
    while True:
        print("Which song would you like to delete from {}\n".format(playlist))
        # Saves the Playlist.json data to a variable called data
        save_file = open(os.path.join(Path(__file__).resolve().parent, "Music", "Playlists.json"), "r")
        data = json.load(save_file)
        save_file.close()
        num = 0
        # Checks how many keys are under playlist then prints the songs
        for songs_json in data[playlist]:
            if num != 0:
                print("{}) ".format(num) + data[playlist][songs_json])
            num += 1
        # if the num var is only at 1 then it detects there is no songs
        if num == 1:
            os.system('cls||clear')
            print("There is no songs in this playlist. Add more songs from the playlist menu below\n")
            # stops the rest from running
            return
        choice = input("\nEnter a number corrosponding to a song or type e to go back to main menu\n").capitalize()
        try:
            # attempts to set the variable from input into a int then checks if it is
            choice = eval(choice)
            if isinstance(choice, int):
                # Saves the Playlist.json data to a dictionary called data
                save_file = open(os.path.join(Path(__file__).resolve().parent, "Music", "Playlists.json"), "r")
                data = dict(json.load(save_file))
                save_file.close()
                itterations = 0
                # itterates through everything in the playlist inside the json file
                for songs in data[playlist].copy():
                    if itterations == int(choice) and int(choice) != 0:
                        # If the music files path exists, delete it
                        if os.path.isfile(os.path.join(Path(__file__).resolve().parent, "Music", f"{playlist}", f"{data[playlist][songs]}.mp3")):
                            os.remove(os.path.join(Path(__file__).resolve().parent, "Music", f"{playlist}", f"{data[playlist][songs]}.mp3"))
                        # deletes the music infomation from the data variable
                        something = 0
                        for i in data[playlist].copy():
                            if itterations == something:
                                data[playlist].pop(i)
                                data[playlist]["song_count"] -= 1
                                print("After Song Count")
                                # Saves the data dictionary to the json file
                                save_file = open(os.path.join(Path(__file__).resolve().parent, "Music", "Playlists.json"), "w")
                                json.dump(data, save_file, indent=6)
                                save_file.close()
                                os.system('cls||clear')
                                return
                            something += 1
                        # stops the rest of the function from running and causing it too return to the playlist menu
                    itterations += 1
                os.system('cls||clear')
                print("Please enter a vaild option\n")
        # if it cannot run the code then this code runs
        except:
            if choice == "E":
                return
            else:
                os.system('cls||clear')
                print("Please enter a vaild option")

def new_playlist():
    global playlist
    os.system('cls||clear')
    while True:
        playlist = str(input("Enter E to exit\nName Of the playlist: "))
        if playlist.capitalize() == "E":
            os.system('cls||clear')
            return
        # checks if the playlist path already exists, if it doesnt it creates a new folder for the playlist
        if not os.path.isdir(os.path.join(Path(__file__).resolve().parent, "Music", f"{playlist}")):
            os.makedirs(os.path.join(Path(__file__).resolve().parent, "Music", f"{playlist}"))
            # adds the playlist to the json file
            new_playlist_name = {playlist: {
                "song_count": 0
                }
            }
            # reads the file and saves all the data to a variable
            save_file = open(os.path.join(Path(__file__).resolve().parent, "Music", "Playlists.json"), "r")
            data = dict(json.load(save_file))
            save_file.close()
            # adds the new playlist to the json file
            data.update(new_playlist_name)
            # Saves the data dictionary to the json file
            save_file = open(os.path.join(Path(__file__).resolve().parent, "Music", "Playlists.json"), "w")
            json.dump(data, save_file, indent=6)
            save_file.close()
            playlist_menu()
            break
        else:
            print("A Playlist with this name already exists\n")
    

def new_song():
    os.system('cls||clear')
    print("Add song to {}\n".format(playlist))
    while True:
        try:
            vid_link = str(input("\nEnter E to exit\nYoutube Link: "))
            if vid_link == "E" or vid_link == "e":
                os.system('cls||clear')
                return
            yt = YouTube(vid_link, on_progress_callback=on_progress)
            name = input("\nSong Name (Leave Blank for video name): ") or yt.title
            if name == "E" or name == "e":
                os.system('cls||clear')
                return
            if not os.path.isfile(os.path.join(Path(__file__).resolve().parent, "Music", f"{playlist}", f"{name}.mp3")):
                yt.title = name
                video = yt.streams.get_audio_only()
                print("Downloading ...")
                video.download(mp3=True, output_path=os.path.join(Path(__file__).resolve().parent, "Music", f"{playlist}")) # pass the parameter mp3=True to save in .mp3
                save_file = open(os.path.join(Path(__file__).resolve().parent, "Music", "Playlists.json"), "r")
                data = dict(json.load(save_file))
                save_file.close()
                data[playlist]["song_count"] += 1
                song_count = 1
                while True:
                    if not "song {}".format(song_count) in data[playlist]:
                        data[playlist]["song {}".format(song_count)] = yt.title
                        break
                    song_count += 1
                save_file = open(os.path.join(Path(__file__).resolve().parent, "Music", "Playlists.json"), "w")
                json.dump(data, save_file, indent=6)
                save_file.close()
                while True:
                    choice = input("{} Has been successfully downloaded. Type E to return to playlist menu or A to download another song: \n".format(yt.title)).capitalize()
                    if choice == "E":
                        os.system('cls||clear')
                        return
                    elif choice == "A":
                        new_song()
                        return
            else:
                print("A song with this name already exists\n")
        except:
            print("Error Please enter a vaild link or name")

def playlist_rename():
    global playlist
    os.system('cls||clear')
    print("What would you like to rename the playlist {} to?".format(playlist))
    while True:
        rename = input("\nNew Name: ")
        if os.path.isdir(os.path.join(Path(__file__).resolve().parent, "Music", f"{playlist}")):
            os.rename(os.path.join(Path(__file__).resolve().parent, "Music", f"{playlist}"), os.path.join(Path(__file__).resolve().parent, "Music", f"{rename}"))
            save_file = open(os.path.join(Path(__file__).resolve().parent, "Music", "Playlists.json"), "r")
            data = json.load(save_file)
            save_file.close()
            data["{}".format(rename)] = data.pop("{}".format(playlist))
            save_file = open(os.path.join(Path(__file__).resolve().parent, "Music", "Playlists.json"), "w")
            json.dump(data, save_file, indent=6)
            save_file.close()
            playlist = rename
            os.system('cls||clear')
            print("Playlist has been renamed\n")
            return
        else:
            print("An unknown error has occured. The playlist save file may be corrupt\nPlease submit an issue on github")

def play_music():
    global playlist, song_continue, playing, choice, shuffling, pause
    playback_state = ""
    current_timestamp = 0
    while True:
        if pause == True:
            if playback_state == "Playing":
                simpleaudio.stop_all()
                end_timestamp = time.time()
                current_timestamp += int(1000 * (end_timestamp - start_timestamp))
                playback_state = "Paused"
            elif playback_state == "Paused":
                slice = current_song_path[current_timestamp:]
                raw_data = slice.raw_data
                music = simpleaudio.play_buffer(raw_data, num_channels=slice.channels, bytes_per_sample=slice.sample_width, sample_rate=slice.frame_rate)
                start_timestamp = time.time()
                playback_state = "Playing"
            pause = False
        if "music" in locals():
            if not music.is_playing() and playback_state == "Playing":
                playing = False
                playback_state = "Stopped"
        while not playing and song_continue == True:
            save_file = open(os.path.join(Path(__file__).resolve().parent, "Music", "Playlists.json"), "r")
            data = json.load(save_file)
            save_file.close()
            n = 0
            for songs_json in data[playlist]:
                if n == int(choice):
                    if os.path.isfile(os.path.join(Path(__file__).resolve().parent, "Music", f"{playlist}", f"{data[playlist][songs_json]}.mp3")):
                        previous_choice = choice
                        current_song_path = AudioSegment.from_file(os.path.join(Path(__file__).resolve().parent, "Music", f"{playlist}", f"{data[playlist][songs_json]}.mp3"))
                    else:
                        print("The song's file does not exist or is corrupted. Please delete it from the playlist menu and redownload it")
                n += 1
                if choice >= len(data[playlist].keys()):
                    choice = 0
                    n = 0
            if shuffling == False:
                choice += 1
            else:
                while True:
                    choice = random.randint(1, len(data[playlist].keys()))
                    if previous_choice == 0:
                        previous_choice = 1
                    if previous_choice != choice:
                        break
            try:
                simpleaudio.stop_all()
                music = playback._play_with_simpleaudio(current_song_path)
                pause = False
                playback_state = "Playing"
                start_timestamp = time.time()
                current_timestamp = 0
            except:
                print("An unknown error has occured.")
            playing = True

def update_shuffling(get_set):
    global shuffling
    save_file = open(os.path.join(Path(__file__).resolve().parent, "Settings.json"), "r")
    data = dict(json.load(save_file))
    save_file.close()
    if get_set == "set":
        for shuffe in data:
            if shuffe == "shuffling":
                if data["shuffling"] == True:
                    data["shuffling"] = False
                    shuffling = False
                elif data["shuffling"] == False:
                    data["shuffling"] = True
                    shuffling = True
        if not "shuffling" in data:
            shuffle_add = {"shuffling": False}
            data.update(shuffle_add)
        save_file = open(os.path.join(Path(__file__).resolve().parent, "Settings.json"), "w")
        json.dump(data, save_file, indent=6)
        save_file.close()
    elif get_set == "get":
        shuffling = data["shuffling"]
    

def playlist_menu():
    global playlist, song_continue, choice, shuffling, playing, pause
    os.system('cls||clear')
    while True:
        print("{}\n".format(playlist))
        # Opens the save file and saves the data to a data variable
        save_file = open(os.path.join(Path(__file__).resolve().parent, "Music", "Playlists.json"), "r")
        data = dict(json.load(save_file))
        save_file.close()
        # Displays all the songs in the playlist
        num = 0
        for songs_json in data[playlist]:
            if num != 0:
                print("{}) ".format(num) + data[playlist][songs_json])
            num += 1
        option = input(f"\np) Pause Song\ns) skip current song\na) New Song\nd) Remove Song\nr) rename playlist\nt) toggle shuffle ({shuffling})\ne) Main Menu\n").capitalize()
        try:
            option = eval(option)
            if isinstance(option, int):
                os.system("cls||clear")
                choice = option
                song_continue = True
        except:
            song_continue = False
            if option == "P":
                os.system("cls||clear")
                pause = True
            elif option == "S":
                simpleaudio.stop_all()
                choice += 1
                playing = False
                song_continue = True
                os.system("cls||clear")
            elif option == "A":
                new_song()
            elif option == "D":
                song_delete_menu()
            elif option == "R":
                playlist_rename()
            elif option == "T":
                update_shuffling("set")
                os.system("cls||clear")
            elif option == "E":
                os.system('cls||clear')
                return
            else:
                os.system("cls||clear")
        simpleaudio.stop_all()

def main_menu():
        global playlist
        os.system('cls||clear')
        while True:
            print("_Open Music App_\n")
            save_file = open(os.path.join(Path(__file__).resolve().parent, "Music", "Playlists.json"), "r")
            data = json.load(save_file)
            save_file.close()
            num = 0
            display = ""
            for playlist_json in data:
                num += 1
                display += "{}) {}\n".format(num, playlist_json)
            choice = input("{}\nc) New Playlist\nd) Delete Playlist\nX) Exit\n".format(display)).capitalize()
            try:
                choice = eval(choice)
                if isinstance(choice, int):
                    save_file = open(os.path.join(Path(__file__).resolve().parent, "Music", "Playlists.json"), "r")
                    data = dict(json.load(save_file))
                    save_file.close()
                    n = 0
                    for playlist_json in data:
                        n += 1
                        if n == int(choice):
                            playlist = playlist_json
                    playlist_menu()
            except:
                if choice == "C":
                    new_playlist()
                elif choice == "D":
                    playlist_delete_menu()
                elif choice == "X":
                    return
                else:
                    print("Please enter a valid option")

# Main Process
os.system('cls||clear')
music_player = threading.Thread(target=play_music, args=())
music_player.start()
update_shuffling("get")
main_menu()
