# Imports
import os, shutil
import simpleaudio
import json
import threading
from pytubefix import YouTube
from pytubefix.cli import on_progress
from pydub import AudioSegment, playback
# Global Variables
playlist = ""
song_continue = True
# Functions

def playlist_delete_menu():
    global playlist
    os.system('cls||clear')
    while True:
        print("Which Playlist would you like to delete?\n\n")
        save_file = open(os.path.join(os.getcwd(), "Music", "Playlists.json"), "r")
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
        choice = input("\nEnter a number corrosponding to a playlist or type x to go back to main menu\n").capitalize()
        try:
            choice = eval(choice)
            if isinstance(choice, int):
                save_file = open(os.path.join(os.getcwd(), "Music", "Playlists.json"), "r")
                data = dict(json.load(save_file))
                save_file.close()
                itterations = 0
                for playlists_json in data.copy():
                    itterations += 1
                    if itterations == int(choice):
                        playlist = playlists_json
                        data.pop(playlist)
                        save_file = open(os.path.join(os.getcwd(), "Music", "Playlists.json"), "w")
                        json.dump(data, save_file, indent=6)
                        save_file.close()
                        if os.path.exists(os.path.join(os.getcwd(), "Music", f"{playlist}")):
                            shutil.rmtree(os.path.join(os.getcwd(), "Music", f"{playlist}"))
                        main_menu()
                raise
        except:
            if choice == "X":
                main_menu()
            else:
                print("Please enter a valid option")

def song_delete_menu():
    global playlist
    os.system('cls||clear')
    while True:
        print("Which song would you like to delete from {}\n".format(playlist))
        # Saves the Playlist.json data to a variable called data
        save_file = open(os.path.join(os.getcwd(), "Music", "Playlists.json"), "r")
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
                save_file = open(os.path.join(os.getcwd(), "Music", "Playlists.json"), "r")
                data = dict(json.load(save_file))
                save_file.close()
                itterations = 0
                # itterates through everything in the playlist inside the json file
                for songs in data[playlist].copy():
                    if itterations == int(choice) and int(choice) != 0:
                        # If the music files path exists, delete it
                        if os.path.isfile(os.path.join(os.getcwd(), "Music", f"{playlist}", f"{data[playlist][songs]}.mp3")):
                            os.remove(os.path.join(os.getcwd(), "Music", f"{playlist}", f"{data[playlist][songs]}.mp3"))
                        # deletes the music infomation from the data variable
                        something = 0
                        for i in data[playlist].copy():
                            if itterations == something:
                                data[playlist].pop(i)
                                data[playlist]["song_count"] -= 1
                                print("After Song Count")
                                # Saves the data dictionary to the json file
                                save_file = open(os.path.join(os.getcwd(), "Music", "Playlists.json"), "w")
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
        playlist = input("Name Of the playlist: ")
        # checks if the playlist path already exists, if it doesnt it creates a new folder for the playlist
        if not os.path.isdir(os.path.join(os.getcwd(), "Music", f"{playlist}")):
            os.makedirs(os.path.join(os.getcwd(), "Music", f"{playlist}"))
            # adds the playlist to the json file
            new_playlist_name = {playlist: {
                "song_count": 0
                }
            }
            # reads the file and saves all the data to a variable
            save_file = open(os.path.join(os.getcwd(), "Music", "Playlists.json"), "r")
            data = dict(json.load(save_file))
            save_file.close()
            # adds the new playlist to the json file
            data.update(new_playlist_name)
            # Saves the data dictionary to the json file
            save_file = open(os.path.join(os.getcwd(), "Music", "Playlists.json"), "w")
            json.dump(data, save_file, indent=6)
            save_file.close()
            playlist_menu()
        else:
            print("A Playlist with this name already exists\n")
    

def new_song():
    os.system('cls||clear')
    print("Add song to {}\n".format(playlist))
    while True:
        try:
            vid_link = str(input("\nEnter E to exit\nYoutube Link: "))
            if vid_link == "E" or vid_link == "e":
                playlist_menu()
            yt = YouTube(vid_link, on_progress_callback=on_progress)
            name = input("\nSong Name (Leave Blank for video name): ") or yt.title
            if name == "E" or name == "e":
                playlist_menu()
            if not os.path.isfile(os.path.join(os.getcwd(), "Music", f"{playlist}", f"{name}.mp3")):
                yt.title = name
                video = yt.streams.get_audio_only()
                video.download(mp3=True, output_path=os.path.join(os.getcwd(), "Music", f"{playlist}")) # pass the parameter mp3=True to save in .mp3
                save_file = open(os.path.join(os.getcwd(), "Music", "Playlists.json"), "r")
                data = dict(json.load(save_file))
                save_file.close()
                data[playlist]["song_count"] += 1
                song_count = 1
                while True:
                    if not "song {}".format(song_count) in data[playlist]:
                        data[playlist]["song {}".format(song_count)] = yt.title
                        break
                    song_count += 1
                save_file = open(os.path.join(os.getcwd(), "Music", "Playlists.json"), "w")
                json.dump(data, save_file, indent=6)
                save_file.close()
                while True:
                    choice = input("{} Has been successfully downloaded. Type E to return to playlist menu or A to download another song: \n".format(yt.title)).capitalize()
                    if choice == "E":
                        playlist_menu()
                    elif choice == "A":
                        new_song()
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
        if os.path.isdir(os.path.join(os.getcwd(), "Music", f"{playlist}")):
            os.rename(os.path.join(os.getcwd(), "Music", f"{playlist}"), os.path.join(os.getcwd(), "Music", f"{rename}"))
            save_file = open(os.path.join(os.getcwd(), "Music", "Playlists.json"), "r")
            data = json.load(save_file)
            save_file.close()
            data["{}".format(rename)] = data.pop("{}".format(playlist))
            save_file = open(os.path.join(os.getcwd(), "Music", "Playlists.json"), "w")
            json.dump(data, save_file, indent=6)
            save_file.close()
            playlist = rename
            os.system('cls||clear')
            print("Playlist has been renamed\n")
            return
        else:
            print("An unknown error has occured. The playlist save file may be corrupt\nPlease submit an issue on github")

def play_music(data, choice):
    global playlist, song_continue
    song_continue = True
    while song_continue == True:
        n = 0
        for songs_json in data[playlist]:
            if n == int(choice):
                if os.path.isfile(os.path.join(os.getcwd(), "Music", f"{playlist}", f"{data[playlist][songs_json]}.mp3")):
                    music_path = AudioSegment.from_file(os.path.join(os.getcwd(), "Music", f"{playlist}", f"{data[playlist][songs_json]}.mp3"))
                    music = playback._play_with_simpleaudio(music_path)
                    print("Before Wait")
                    music.wait_done()
                    print("After Wait")
                else:
                    print("The song's file does not exist or is corrupted. Please delete it from the playlist menu and redownload it")
            n += 1
        if choice == len(data[playlist].keys()):
            choice = 0
        choice += 1

def playlist_menu():
    global playlist, music_thread, song_continue
    os.system('cls||clear')
    while True:
        print("{}\n".format(playlist))
        # Opens the save file and saves the data to a data variable
        save_file = open(os.path.join(os.getcwd(), "Music", "Playlists.json"), "r")
        data = json.load(save_file)
        save_file.close()
        # Displays all the songs in the playlist
        num = 0
        for songs_json in data[playlist]:
            if num != 0:
                print("{}) ".format(num) + data[playlist][songs_json])
            num += 1
        choice = input("\na) New Song\nd) Remove Song\ns) skip current song\nr) rename playlist\nt) toggle shuffle (ON)\ne) Main Menu\n").capitalize()
        try:
            choice = eval(choice)
            if isinstance(choice, int):
                save_file = open(os.path.join(os.getcwd(), "Music", "Playlists.json"), "r")
                data = dict(json.load(save_file))
                save_file.close()
                simpleaudio.stop_all()
                song_continue = False
                music_thread = threading.Thread(target= play_music, args= (data, choice))
                music_thread.start()
                os.system('cls||clear')
        except:
            if choice == "A":
                new_song()
            elif choice == "D":
                song_delete_menu()
            elif choice == "S":
                print("ADD SKIPPING SONGS!")
            elif choice == "R":
                playlist_rename()
            elif choice == "T":
                print("ADD TOGGLE SHUFFLING")
            elif choice == "E":
                main_menu()

def main_menu():
        global playlist
        os.system('cls||clear')
        while True:
            print("_Open Music App_\n")
            save_file = open(os.path.join(os.getcwd(), "Music", "Playlists.json"), "r")
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
                    save_file = open(os.path.join(os.getcwd(), "Music", "Playlists.json"), "r")
                    data = dict(json.load(save_file))
                    save_file.close()
                    n = 0
                    for playlist_json in data:
                        n += 1
                        print(choice)
                        if n == int(choice):
                            playlist = playlist_json
                    playlist_menu()
                    break
            except:
                if choice == "C":
                    new_playlist()
                elif choice == "D":
                    playlist_delete_menu()
                elif choice == "X":
                    exit()
                else:
                    print("Please enter a valid option")

# Main Process
os.system('cls||clear')
main_menu()