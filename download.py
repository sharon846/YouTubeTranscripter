from datetime import timedelta
import os
import whisper
from pytube import Playlist
from pytube import YouTube
import torch

def transcribe_audio(path, file_name):
    model = whisper.load_model("large") # Change this to your desired model
    print("Whisper model loaded.")
    transcribe = model.transcribe(audio=path)
    segments = transcribe['segments']

    for segment in segments:
        startTime = str(0)+str(timedelta(seconds=int(segment['start'])))+',000'
        endTime = str(0)+str(timedelta(seconds=int(segment['end'])))+',000'
        text = segment['text']
        segmentId = segment['id']+1
        segment = f"{segmentId}\n{startTime} --> {endTime}\n{text[1:] if text[0] == ' ' else text}\n\n"

        srtFilename = f'{file_name}.srt'
        with open(srtFilename, 'a', encoding='utf-8') as srtFile:
            srtFile.write(segment)

    del model.encoder
    del model.decoder
    torch.cuda.empty_cache()
    return srtFilename

def download_audio_as_wav(yt, video_title):
    stream = yt.streams.filter(only_audio=True).first()
    if stream:
        print(f"Downloading audio for '{video_title}'...")
        stream.download(filename=f"{video_title}.mp3")
        # Here you can convert the downloaded mp3 file to WAV if you prefer, using a library like pydub.
        # The conversion process requires the pydub library and ffmpeg.
        # Example code for conversion:
        # from pydub import AudioSegment
        # audio = AudioSegment.from_mp3(f"{video_title}.mp3")
        # audio.export(f"{video_title}.wav", format="wav")
        print(f"Audio downloaded for '{video_title}', starts converting..")
        transcribe_audio(f"{video_title}.mp3", video_title)
        os.remove(f"{video_title}.mp3")
    else:
        print(f"No audio available for '{video_title}'")

def main():
    playlist_link = input("Enter the link to the YouTube playlist: ")
    playlist = Playlist(playlist_link)
    playlist._video_regex = r"\"url\":\"(/watch\?v=[\w-]*)"
    videos = playlist.video_urls
    all = False

    for video_url in videos:
        yt = YouTube(video_url)
        video_title = yt.title
        if not all:
            print(f"Video Title: {video_title}")
            choice = input("Do you want to (s)kip, (p)roceed or download (a)ll? (s/p/a): ").lower()
        
            if choice == "a":
                all = True

        if choice == "s":
            print(f"Skipping '{video_title}'")
        elif choice == "p" or all:
            download_audio_as_wav(yt, video_title)
        else:
            print("Invalid choice. Skipping...")

if __name__ == "__main__":
    main()



#model = whisper.load_model("large")
#result = model.transcribe("output_000.wav")
#print(result["text"])
