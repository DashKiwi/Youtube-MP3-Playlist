@echo off
if not "%1"=="am_admin" (
    powershell -Command "Start-Process -Verb RunAs -FilePath '%0' -ArgumentList 'am_admin'"
    exit /b
)
@echo on

pip uninstall pytubefix -y
pip install pytubefix
pip install wheel
pip install pydub
pip install simpleaudio
pip install keyboard
Powershell.exe -executionpolicy remotesigned -File "%~dp0ffmpeg-requirements.ps1"