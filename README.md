# YouTube MP3 Playlist

YouTube MP3 Playlist is a small python program to allow you to download and play YouTube videos in an audio format, organized by playlists
## Installation

You can either run the setup.bat file found in the top folder (will ask for administrator) of the repository or manually download the required library's below.

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the needed library's.

```bash
pip install pytubefix
pip install wheel
pip install pydub
pip install simpleaudio
pip install keyboard
```

For linux you may have to run the 'pip install keyboard' command with sudo E.g. 'sudo pip install keyboard'

You may need to install ffmpeg for the program to run. To do so you can go to [ffmpeg download](https://www.ffmpeg.org/download.html) and follow the installation process.
## Usage

To automatically start it you can run the start.bat file which will start the program or run the code below to start it manually

```bash
cd yourdrive:\pathtofolder
python Main.py
```
alternatively you could run the python file in your own IDE whatever you do it is up too you!

Keybinds:
To choose a keybind to pause the program, open the Settings.json file and change pause_button to your chosen keybind. Usually a keybind will look like "p" or you can combine keys to make a keybind such as "ctrl+p". Search up 'keyboard python library keycodes' to find keycodes for the keybinds.

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)
