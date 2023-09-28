# YouTubeTranscripter
Transcript an entire playlist from YouTube, based on [OpenAI Whisper](https://github.com/openai/whisper).
<br/>

This repo's scripts have since been modified to use [faster-whisper](https://github.com/guillaumekln/faster-whisper).
Note: pytube seems to be a bit borked, 

## Demo
Example for subtitles (in Hebrew) obtained from the regular whisper model is [Tutorial 10 - Cross Validation](https://www.youtube.com/watch?v=LHUXrLS8Xzc)

## Requirments:
1. You need a GPU that uses CUDA, so that means a modern Nvidia GPU with a decent amount of VRAM (check whisper's and faster-whisper's requirements).
2. You need to make sure you have met the requirements of Whisper. That means having an updated version of CUDA Toolkit, adding its bin folder to your system path (CRUCIAL!), etc.

## Install:
1. `git clone`
2. `cd YouTubeTranscripter`
3. `pip install -r requirements.txt`
4. Run `python download.py`.

## Useage:
download-faster.ipynb is meant for Google Colab.

There are several .py files:
- TranscribeAudioFile.py is meant to transcribe a single audio file. Simply run the script with an argument that contains the path of the audio file you wish to transcribe (Useage example: python TranscribeAudioFile.py "SomeAudioFile.wav").
- TranscribeYouTubePlaylist.py is the one that can transcribe an entire YouTube playlist. It has no arguments, just follow the instructions.
- download.py is an older, deprecated version of the playlist script that uses the original whisper model.

## NOTE: The playlist script doesn't seem to continue after it's done with the first video for some reason, this problem is recent.