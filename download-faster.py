from pytube import Playlist
from pytube import YouTube

from faster_whisper import WhisperModel
import torch

from datetime import timedelta
from tqdm import tqdm 
import os


def transcribe_audio(path, file_name):
	# Run on GPU with FP16
	model = WhisperModel("large-v2", device="cuda", compute_type="float16")

	# or run on GPU with INT8
	# model = WhisperModel("large-v2", device="cuda", compute_type="int8_float16")
	# or run on CPU with INT8
	# model = WhisperModel("large-v2", device="cpu", compute_type="int8")
	
	print("Whisper model loaded.")
	
	segments, info = model.transcribe(path, beam_size=5)
	print("Detected language '%s' with probability %f" % (info.language, info.language_probability))
	
	segmentId = 1
	text = ""
	for segment in tqdm(segments):
		startTime = str(0)+str(timedelta(seconds=int(segment.start)))+',000'
		endTime = str(0)+str(timedelta(seconds=int(segment.end)))+',000'
		txt = segment.text
		text = text + f"{segmentId}\n{startTime} --> {endTime}\n{txt[1:] if txt[0] == ' ' else txt}\n\n"
		segmentId+=1

	srtFilename = f'{file_name}.srt'
	with open(srtFilename, 'a', encoding='utf-8') as srtFile:
		srtFile.write(text)

	#optional, to clean cache
	torch.cuda.empty_cache()

	return file_name

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
			choice = input("Do you want to (e)xit, (s)kip, (p)roceed or download (a)ll? (s/p/a): ").lower()
		
			if choice == "a":
				all = True
		if choice == "e":
			return;
		if choice == "s":
			print(f"Skipping '{video_title}'")
		elif choice == "p" or all:
			download_audio_as_wav(yt, video_title)
		else:
			print("Invalid choice. Skipping...")

if __name__ == "__main__":
	main()
