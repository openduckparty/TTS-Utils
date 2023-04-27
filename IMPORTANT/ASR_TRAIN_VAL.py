import os
import sys
import random
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
                with open(os.path.join(top_folder, f"{sys.argv[1]}_train.txt"), "a", encoding='utf-8') as all_transcript_file:
                    all_transcript_file.writelines(f"{wav_folder}/{wav_file}|{speaker_id}|{result['text'].strip()}\n")

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
    
    input_file = f'./{sys.argv[1]}_train.txt'
    output_file = f'./{sys.argv[1]}_val.txt'

    select_random_lines(input_file, output_file)

def select_random_lines(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as file:
        all_lines = file.readlines()
    
    total_lines = len(all_lines)
    lines_to_select = int(total_lines / 100)
    if(lines_to_select == 0):
        lines_to_select = 1
    selected_lines = random.sample(all_lines, lines_to_select)

    with open(output_file, 'w', encoding='utf-8') as file:
        for line in selected_lines:
            file.write(line)

if __name__ == "__main__":
    main()
