from faster_whisper import WhisperModel
from datetime import timedelta
from tqdm import tqdm 

model_size = "large-v2"

# Run on GPU with FP16
model = WhisperModel(model_size, device="cuda", compute_type="float16")

# or run on GPU with INT8
# model = WhisperModel(model_size, device="cuda", compute_type="int8_float16")
# or run on CPU with INT8
# model = WhisperModel(model_size, device="cpu", compute_type="int8")

segments, info = model.transcribe("/content/drive/MyDrive/deep learning/output_000.wav", beam_size=5)
print("Detected language '%s' with probability %f" % (info.language, info.language_probability))

segmentId = 1
text = ""
for segment in tqdm(segments):
    startTime = str(0)+str(timedelta(seconds=int(segment.start)))+',000'
    endTime = str(0)+str(timedelta(seconds=int(segment.end)))+',000'
    txt = segment.text
    text = text + f"{segmentId}\n{startTime} --> {endTime}\n{txt[1:] if txt[0] == ' ' else txt}\n\n"
    segmentId+=1
    
srtFilename = f'subtitles.srt'
with open(srtFilename, 'a', encoding='utf-8') as srtFile:
  srtFile.write(text)

#for segment in segments:
#    print("[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text))
