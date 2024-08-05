# Imports
import os
import simpleaudio
import json
from pytubefix import YouTube
from pytubefix.cli import on_progress
from pydub import AudioSegment, playback
# Global Variables
playlist = ""

# Functions

def new_playlist():
    global playlist
    # clears the console
    os.system('cls')
    while True:
        # Gets what you want to name the playlist
        playlist = input("Name Of the playlist: ")
        # checks if the playlist path already exists, if it doesnt it creates a new folder for the playlist
        if not os.path.isdir(r".\Music\{}".format(playlist)):
            os.makedirs(r".\Music\{}".format(playlist))
            # adds the playlist to the json file
            new_playlist_name = {playlist: {
                "song_count": 0
                }
            }
            # reads the file and gets all the data
            save_file = open(r".\Music\Playlists.json", "r")
            data = dict(json.load(save_file))
            save_file.close()
            # adds the new playlist to the json file
            data.update(new_playlist_name)
            print(data)
            # gains write acces to the json file
            save_file = open(r".\Music\Playlists.json", "w")
            # rewrites the json file with all the data
            json.dump(data, save_file, indent=6)
            # saves the file
            save_file.close()
            # moves to the playlist menu
            playlist_menu()
        else:
            print("A Playlist with this name already exists\n")
    

def new_song():
    os.system('cls')
    print("Add song to {}\n".format(playlist))
    vid_link = str(input("\nYoutube Link: "))
    yt = YouTube(vid_link, on_progress_callback=on_progress)
    name = input("\nSong Name (Leave Blank for video name): ") or yt.title
    yt.title = name
    video = yt.streams.get_audio_only()
    video.download(mp3=True, output_path=".\Music\{}".format(playlist)) # pass the parameter mp3=True to save in .mp3
    save_file = open(r".\Music\Playlists.json", "r")
    data = dict(json.load(save_file))
    save_file.close()
    data[playlist]["song_count"] += 1
    data[playlist]["song {}".format(data[playlist]["song_count"])] = yt.title
    save_file = open(r".\Music\Playlists.json", "w")
    json.dump(data, save_file, indent=6)
    save_file.close()
    while True:
        choice = input("{} Has been successfully downloaded type e it return to playlist menu: ".format(yt.title)).capitalize()
        if choice == "E":
            playlist_menu()

def playlist_menu():
    global playlist
    os.system('cls')
    print("{}\n".format(playlist))
    # Gives read access to the file
    save_file = open(r".\Music\Playlists.json", "r")
    # loads the data of the json file
    data = json.load(save_file)
    # Displays all the songs in the play list
    num = 0
    for i in data[playlist]:
        if num != 0:
            print("{}) ".format(num) + data[playlist][i])
        num += 1
    # choose what the user wants to play/do
    while True:
        choice = input("\na) New Song\nd) Remove Song\ns) skip current song\nr) rename playlist\nt) toggle shuffle (ON)\ne) Main Menu\n").capitalize()
        try:
            choice = eval(choice)
            if isinstance(choice, int):
                    save_file = open(r".\Music\Playlists.json", "r")
                    data = dict(json.load(save_file))
                    save_file.close()
                    n = 0
                    for i in data:
                        n += 1
                        if n == int(choice):
                            print("Yay its working")
                    # Put the code you want to run the music here
        except:
            # checks all the user choices
            if choice == "A":
                new_song()
            elif choice == "D":
                print("ADD REMOVE SONG")
            elif choice == "S":
                print("ADD SKIPPING SONGS!")
            elif choice == "R":
                print("ADD RENAMING PLAYLISTS")
            elif choice == "T":
                print("ADD TOGGLE SHUFFLING")
            elif choice == "E":
                main_menu()

def main_menu():
        global playlist
        os.system('cls')
        print("_Open Music App_\n\n")
        save_file = open(r".\Music\Playlists.json", "r")
        data = json.load(save_file)
        num = 0
        display = ""
        for i in data:
            num += 1
            display += "{}) {}\n".format(num, i)
        while True:
            choice = input("{}\nc) New Playlist\nX) Exit\n".format(display)).capitalize()
            try:
                choice = eval(choice)
                if isinstance(choice, int):
                    save_file = open(r".\Music\Playlists.json", "r")
                    data = dict(json.load(save_file))
                    save_file.close()
                    n = 0
                    for i in data:
                        n += 1
                        print(choice)
                        if n == int(choice):
                            playlist = i
                    print(playlist)
                    playlist_menu()
                    break
            except:
                if choice == "C":
                    new_playlist()
                elif choice == "X":
                    os.close
                else:
                    print("Please enter a valid option")

# Main Process
os.system('cls')
main_menu()