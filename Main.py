# Imports
import os, shutil
import simpleaudio
import json
from pytubefix import YouTube
from pytubefix.cli import on_progress
from pydub import AudioSegment, playback
# Global Variables
playlist = ""
# Functions

def playlist_delete_menu():
    global playlist
    os.system('cls')
    print("Which Playlist would you like to delete?\n\n")
    save_file = open(r".\Music\Playlists.json", "r")
    data = json.load(save_file)
    save_file.close()
    num = 0
    for i in data:
        num += 1
        print("{}) {}".format(num, i))
    if num == 0:
        os.system('cls')
        print("You have no playlists. Create a new one in the menu below\n")
        return
    while True:
        choice = input("\nEnter a number corrosponding to a playlist or type x to go back to main menu\n").capitalize()
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
                        playlist = i
                        data.pop(playlist)
                        save_file = open(r".\Music\Playlists.json", "w")
                        json.dump(data, save_file, indent=6)
                        save_file.close()
                        if os.path.exists(r".\Music\{}".format(playlist)):
                            shutil.rmtree(r".\Music\{}".format(playlist))
                        main_menu()
                raise
        except:
            if choice == "X":
                main_menu()
            else:
                print("Please enter a valid option")

def song_delete_menu():
    global playlist
    os.system('cls')
    # Asks which song they would like to delete from the playlist, including name
    print("Which song would you like to delete from {}\n".format(playlist))
    # opens the save file with read access
    save_file = open(r".\Music\Playlists.json", "r")
    # saves the json file in the data variable
    data = json.load(save_file)
    # closes the save file
    save_file.close()
    num = 0
    # Checks how many layers are under playlist
    for i in data[playlist]:
        # only prints if after the first itteration
        # The reason for this is that the song_count would be printed
        if num != 0:
            # prints the playlist songs
            print("{}) ".format(num) + data[playlist][i])
        # adds too num for a counter
        num += 1
    # if the num var is only at 1 then it detects there is no songs
    if num == 1:
        os.system('cls')
        print("There is no songs in this playlist. Add more songs from the playlist menu below\n")
        # stops the rest of the function from running and causing it too return to the playlist menu
        return
    # if there is more than 0 songs this runs
    while True:
        # asks the user what they want to do
        choice = input("\nEnter a number corrosponding to a song or type x to go back to main menu\n").capitalize()
        # attempts to run the following code
        try:
            # attempts to set the variable from input into a int
            choice = eval(choice)
            # checks if the choice is a int
            if isinstance(choice, int):
                # opens save file with read access
                save_file = open(r".\Music\Playlists.json", "r")
                # saves a dictionary with the json data
                data = dict(json.load(save_file))
                # closes the save file
                save_file.close()
                n = 0
                # itterates through everything in the playlist inside the json file
                for i in data[playlist]:
                    # checks if n is the same as the choice the user chose
                    # Starts before the count to ignore the song count in the json
                    if n == int(choice):
                        # checks if the path with the music file they are wanting to delete exists
                        if os.path.isdir(r".\\Music\\{}\\{}.mp3".format(playlist, data[playlist][i])):
                            # deletes the music file
                            os.remove(r".\\Music\\{}\\{}.mp3".format(playlist, data[playlist][i]))
                        # deletes the music infomation from the data variable
                        del data[playlist]["song {}".format(n)]
                        # changes the song_count in the data variable by -1
                        data[playlist]["song_count"] -= 1
                        # opens the save file with write access
                        save_file = open(r".\Music\Playlists.json", "w")
                        # rewrites the json file with everything inside the data variable
                        json.dump(data, save_file, indent=6)
                        # saves the json file with all the new infomation
                        save_file.close()
                        os.system('cls')
                        # stops the rest of the function from running and causing it too return to the playlist menu
                        return
                    n += 1
                raise
        # if it cannot run the code then this code runs
        except:
            # checks if the choice was "X"
            if choice == "X":
                # returns to the playlist menu
                return
            else:
                # A vaild option has not been entered so send a error message and let the user retry
                print("Please enter a vaild option")


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
        choice = input("{} Has been successfully downloaded. Type E to return to playlist menu: \n".format(yt.title)).capitalize()
        if choice == "E":
            playlist_menu()

def playlist_rename():
    global playlist
    os.system('cls')
    print("What would you like to rename the playlist {} to?".format(playlist))
    while True:
        rename = input("\nNew Name: ")
        if os.path.isdir(r".\\Music\\{}".format(playlist)):
            os.rename(r".\\Music\\{}".format(playlist), r".\\Music\\{}".format(rename))
            save_file = open(r".\Music\Playlists.json", "r")
            data = json.load(save_file)
            save_file.close()
            data["{}".format(rename)] = data.pop("{}".format(playlist))
            save_file = open(r".\Music\Playlists.json", "w")
            json.dump(data, save_file, indent=6)
            save_file.close()
            playlist = rename
            os.system('cls')
            print("Playlist has been renamed\n")
            return
        else:
            print("An unknown error has occured. The playlist save file may be corrupt\nPlease submit an issue on github")



def playlist_menu():
    global playlist
    os.system('cls')
    while True:
        print("{}\n".format(playlist))
        # Gives read access to the file
        save_file = open(r".\Music\Playlists.json", "r")
        # loads the data of the json file
        data = json.load(save_file)
        save_file.close()
        # Displays all the songs in the play list
        num = 0
        for i in data[playlist]:
            if num != 0:
                print("{}) ".format(num) + data[playlist][i])
            num += 1
        # choose what the user wants to play/do
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
        os.system('cls')
        while True:
            print("_Open Music App_\n")
            save_file = open(r".\Music\Playlists.json", "r")
            data = json.load(save_file)
            save_file.close()
            num = 0
            display = ""
            for i in data:
                num += 1
                display += "{}) {}\n".format(num, i)
            choice = input("{}\nc) New Playlist\nd) Delete Playlist\nX) Exit\n".format(display)).capitalize()
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
                    playlist_menu()
                    break
            except:
                if choice == "C":
                    new_playlist()
                elif choice == "D":
                    playlist_delete_menu()
                elif choice == "X":
                    os.close
                else:
                    print("Please enter a valid option")

# Main Process
os.system('cls')
main_menu()