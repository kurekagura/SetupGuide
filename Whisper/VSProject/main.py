import os
import whisper

download_root="./models"

#model = whisper.load_model("base", download_root = download_root)
model = whisper.load_model("small", download_root = download_root)
#model = whisper.load_model("large", download_root = download_root)

userprofile = os.environ["USERPROFILE"]
filename = "レコーディング.m4a"
filepath = os.path.join(userprofile, r"Documents\サウンド レコーディング", filename)
print(filepath)

audio = whisper.load_audio(filepath)
audio = whisper.pad_or_trim(audio)

mel = whisper.log_mel_spectrogram(audio).to(model.device)

# detect the spoken language
_, probs = model.detect_language(mel)
print(f"Detected language: {max(probs, key=probs.get)}")

# decode the audio
lang = "ja" #en js
#options = whisper.DecodingOptions()
options = whisper.DecodingOptions(language=lang, without_timestamps=True)

result = whisper.decode(model, mel, options)

# print the recognized text
print(result.text)

# Write into a text file
outfilepath = os.path.join(userprofile, r"Documents\サウンド レコーディング", "whisper_results.txt")
with open(outfilepath, "a") as f:
    f.write(result.text)
    f.write('\n')
