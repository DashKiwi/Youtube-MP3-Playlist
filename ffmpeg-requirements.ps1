if (Test-Path "C:\ffmpeg") {
    exit
}
else {
    New-Item -Type Directory -Path C:\ffmpeg ; Set-Location C:\ffmpeg
    curl.exe -L 'https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip' -o 'ffmpeg.zip'
    Expand-Archive .\ffmpeg.zip -Force -Verbose
    Get-ChildItem -Recurse `
        -Path .\ffmpeg\ -Filter *.exe |
        ForEach-Object {
            Move-Item $_ -Destination .\ -Verbose
        }
    Remove-Item .\ffmpeg\ -Recurse
    Remove-Item .\ffmpeg.zip
    [System.Environment]::SetEnvironmentVariable(
        "PATH",
        "C:\ffmpeg\;$([System.Environment]::GetEnvironmentVariable('PATH','MACHINE'))",
        "Machine"
    )
    $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine")
}