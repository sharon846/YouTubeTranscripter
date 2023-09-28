from faster_whisper import WhisperModel
import torch

from datetime import timedelta
from tqdm import tqdm 
import os
import sys

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

def main():
	if len(sys.argv) > 1:
		audio_file = sys.argv[1]
		print(f"Starting to transcribe {audio_file}")
		transcribe_audio(audio_file, audio_file)   


if __name__ == "__main__":
	main()
