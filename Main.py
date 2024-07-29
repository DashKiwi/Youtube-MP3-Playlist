import os
import simpleaudio
from pytubefix import YouTube
from pytubefix.cli import on_progress
from pydub import AudioSegment, playback

def new_download():
    vid_link = str(input("Enter the URL of the video you want to download: \n>> "))

    yt = YouTube(vid_link, on_progress_callback=on_progress)

    destination = str(input("Enter the destination (leave blank for current directory): \n>> ")) or '.\Music'
    
    video = yt.streams.get_audio_only()
    video.download(mp3=True, output_path=destination) # pass the parameter mp3=True to save in .mp3

    print(yt.title + " has been successfully downloaded.")

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

def playlist():
    print("Playlist {}\n\n")
    print("1) Song 1 - 3:45\n2) Song 2 - 5:33 PLAYING\n3) Song 3 - 2:13\n4) Song 4 - 7:45")
    input("a) New Song\nd) Remove Song\ns) skip current song\nr) rename playlist\nt) toggle shuffle (ON)\ne) Main Menu\n\n PLAYING: Land Down Under")

def new_playlist():
    os.system('cls')
    new_playlist_name = [input("Name Of the playlist: ")]
    playlists = open(".\Music\Setting.txt")
    playlists.write(new_playlist_name)

def new_song():
    os.system('cls')
    print("Add song to playlist {}\n")
    vid_link = str(input("\nYoutube Link: "))
    yt = YouTube(vid_link, on_progress_callback=on_progress)
    yt.title = input("\nName: ")
    video = yt.streams.get_audio_only()
    video.download(mp3=True, output_path=".\Music") # pass the parameter mp3=True to save in .mp3
    print(yt.title + " Has been successfully downloaded")

def main_menu():
    os.system('cls')
    choice = input("_Music Player App_\n\n1) #Test Start\n2) #playlist b\n3) #playlist c\n\nc) New Playlist\nX) Exit\n")
    if choice == "1" or choice == "2" or choice == "3":
        start()
    elif choice == "C":
        new_playlist()
    elif choice == "X":
        os.close

main_menu()