import os
from pytubefix import YouTube
from pytubefix.cli import on_progress
from pydub import AudioSegment
from pydub.playback import play

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
        new_download()
    elif usr_choice == 2:
        Music = AudioSegment.from_file("Arms Shouldn't Look Like This.mp3", format="mp3")
        play(Music)

start()