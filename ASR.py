import os
import whisper

model = whisper.load_model("large")
lang_lst = ['ja', 'japanese']

def process_wav_files(speaker_id, wav_folder, transcript_file, top_folder):
    with open(transcript_file, "w", encoding='utf-8') as f:
        for wav_file in sorted(os.listdir(wav_folder)):
            if wav_file.endswith(".wav"):
                file_path = os.path.join(wav_folder, wav_file)
                with open(file_path, "rb") as audio_file:
                    result = model.transcribe(file_path)
                print(f"{wav_folder}/{wav_file}|{speaker_id}|{result['text'].strip()}")
                f.writelines(f"{wav_folder}/{wav_file}|{speaker_id}|{result['text'].strip()}\n")
                with open(os.path.join(top_folder, "blueac.txt"), "a", encoding='utf-8') as blueac_file:
                    blueac_file.writelines(f"{wav_folder}/{wav_file}|{speaker_id}|{result['text'].strip()}\n")

def main():
    top_folder = "./"
    speaker_id = 0

    for folder in sorted(os.listdir(top_folder)):
        folder_path = os.path.join(top_folder, folder)
        if os.path.isdir(folder_path):
            wav_folder = os.path.join(folder_path, "wavs")
            transcript_file = os.path.join(folder_path, "transcript.txt")
            process_wav_files(speaker_id, wav_folder, transcript_file, top_folder)
            speaker_id += 1

if __name__ == "__main__":
    main()
