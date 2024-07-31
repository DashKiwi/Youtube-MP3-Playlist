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
def new_download():
    global playlist
    # gets the wanted link
    vid_link = str(input("Enter the URL of the video you want to download:\n"))
    # Gets the video
    yt = YouTube(vid_link, on_progress_callback=on_progress)
    # Chooses where to store
    destination = ".\Music\{}".format(playlist)
    # Downloads the video
    video = yt.streams.get_audio_only()
    video.download(mp3=True, output_path=destination) # pass the parameter mp3=True to save in .mp3
    # Says when its been downloaded
    while True:
        choice = string_checker(yt.title + " has been successfully downloaded. enter e to return to Playlist menu")
        if choice == "E":
            playlist_menu()
            break

def string_checker(prompt):
    while True:
        try:
            return(str(input(prompt).capitalize()))
        except:
            print("Please enter a valid request")

def start():
    usr_choice = int(input("Do you want to\n1. Download new music\n2. listen to downloaded music\n>>"))
    if usr_choice == 1:
        new_song()
    elif usr_choice == 2:
        Music = AudioSegment.from_file(".\Music\Arms Shouldn't Look Like This.mp3", format="mp3")
        play_obj = simpleaudio.WaveObject(Music.raw_data, num_channels= Music.channels, bytes_per_sample= Music.sample_width, sample_rate= Music.frame_rate)
        playing = play_obj.play()
        choice = input("DaDitDaDit")
        if choice == "a":
            playing.stop()
        playing.wait_done()

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
    for j in data[playlist]:
        if num != 0:
            num += 1
            print("{}) ".format(num) + data[playlist][j])
    # choose what the user wants to play/do
    choice = string_checker("\na) New Song\nd) Remove Song\ns) skip current song\nr) rename playlist\nt) toggle shuffle (ON)\ne) Main Menu")
    # checks all the user choices
    if choice == "A":
        new_download()

def new_playlist():
    global playlist
    # clears the console
    os.system('cls')
    # Gets what you want to name the playlist
    playlist = input("Name Of the playlist: ")
    # adds the playlist to the json file
    new_playlist_name = {playlist: {
        "song_count": "0"
    }}
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
    # checks if the playlist path already exists, if it doesnt it creates a new folder for the playlist
    if not os.path.isdir(r".\Music\{}".format(playlist)):
        os.makedirs(r".\Music\{}".format(playlist))
    # moves to the playlist menu
    playlist_menu()
    

def new_song():
    os.system('cls')
    print("Add song to {}\n".format(playlist))
    vid_link = str(input("\nYoutube Link: "))
    yt = YouTube(vid_link, on_progress_callback=on_progress)
    yt.title = string_checker("\nSong Name: ")
    video = yt.streams.get_audio_only()
    video.download(mp3=True, output_path=".\Music\{}".format(playlist)) # pass the parameter mp3=True to save in .mp3
    save_file = open(r".\Music\Playlists.json", "r")
    data = dict(json.load(save_file))
    save_file.close()
    data[playlist]["song_count"] += 1
    data[playlist]["song{}".format(data[playlist]["song_count"])] = yt.title
    save_file = open(r".\Music\Playlists.json", "w")
    json.dump(data, save_file, indent=6)
    save_file.close()

    while True:
        choice = string_checker("{} Has been successfully downloaded type e it return to playlist menu".format(yt.title))
        if choice == "E":
            playlist_menu()
        

def main_menu():
    os.system('cls')
    save_file = open(r".\Music\Playlists.json", "r")
    data = json.load(save_file)
    num = 0
    for i in data:
        num += 1
        print("{}) ".format(num) + data[i])
    choice = string_checker("_Open Music App_\n\n1) #Test Start\n2) #playlist b\n3) #playlist c\n\nc) New Playlist\nX) Exit\n")
    if choice == "1" or choice == "2" or choice == "3":
        start()
    elif choice == "C":
        new_playlist()
    elif choice == "X":
        os.close

# Main Process
os.system('cls')
main_menu()