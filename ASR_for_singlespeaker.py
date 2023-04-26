import whisper
import os

model = whisper.load_model("large") # large
lang_lst = ['ko', 'korean']

wav_dir_loc = '/content/drive/MyDrive/tts_datasets/latte/wavs'
metadata_loc = '/content/drive/MyDrive/tts_datasets/latte/transcript.txt'

lst = os.listdir(wav_dir_loc)

for idx, i in enumerate(lst):
    result = model.transcribe(f"{wav_dir_loc}/{i}")
    if result['language'].lower() in lang_lst:
        
        print(idx, i, result['text'])

        f = open(metadata_loc, 'a', encoding='utf-8')
        f.writelines(f"{wav_dir_loc}/{i}|{result['text'].strip()}\n")
        f.close()
