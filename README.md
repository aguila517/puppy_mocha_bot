Puppy MochaBot is a lite version of MochaBot that'll only check Torrey Pines.

Pre-requisite:
Choco:
@"%SystemRoot%\System32\WindowsPowerShell\v1.0\powershell.exe" -NoProfile -InputFormat None -ExecutionPolicy Bypass -Command "[System.Net.ServicePointManager]::SecurityProtocol = 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))" && SET "PATH=%PATH%;%ALLUSERSPROFILE%\chocolatey\bin"

Python@3.9.6
https://www.python.org/downloads/release/python-396/

Windows:
choco install ffmpeg

Mac:
brew install ffmpeg

Installation:
python3 -m venv myenv
<Windows> myenv/Scripts/activate.bat
<Linux> source myenv/bin/activate 
pip3 install -r requirements.txt
python3 bot_health_check.py
