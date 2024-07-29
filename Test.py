from pytubefix import YouTube
from pytubefix.cli import on_progress

vid_link = str(input("Enter the URL of the video you want to download: \n>> "))

yt = YouTube(vid_link, on_progress_callback=on_progress)

destination = str(input("Enter the destination (leave blank for current directory): \n>> ")) or '.\Music'

video = yt.streams.get_highest_resolution()
video.download(output_path=destination) # pass the parameter mp3=True to save in .mp3

print(yt.title + " has been successfully downloaded.")