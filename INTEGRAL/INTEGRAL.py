#sys.argv[1] = ex) ko, ja, en, zh
#sys.argv[2] = ALL transcription saved in this txt. insert model name
#sys.argv[3] = sample rate

import os
import glob
import shutil
import numpy as np
import random
import whisper
import sys
import time
import wave
import contextlib
import subprocess
import json
import ast
from tqdm import tqdm
from shutil import rmtree
from scipy.io import wavfile
from langdetect import detect


def preprocessing_code(sample_rate):
    def convert_mp3_to_wav(root_dir):
        if not os.path.isdir(root_dir):
            raise ValueError("The provided root directory does not exist.")

        for subdir, dirs, files in os.walk(root_dir):
            if subdir == root_dir:  # Skip the root directory
                continue

            wavs_dir = os.path.join(subdir, "wavs")
            if not os.path.exists(wavs_dir):
                os.makedirs(wavs_dir)

            for file in files:
                if file.endswith(".mp3"):
                    mp3_filepath = os.path.join(subdir, file)
                    wav_filename = os.path.splitext(file)[0] + ".wav"
                    wav_filepath = os.path.join(wavs_dir, wav_filename)
                    print(f"Converting {mp3_filepath} to {wav_filepath}...")

                    try:
                        subprocess.run(["ffmpeg", "-i", mp3_filepath, "-ar", str(sample_rate), "-ac", "1", wav_filepath], check=True)
                    except subprocess.CalledProcessError as e:
                        print(f"Error while converting {mp3_filepath} to {wav_filepath}: {e}")

                elif file.endswith(".wav"):
                    wav_filepath = os.path.join(subdir, file)
                    dest_filepath = os.path.join(wavs_dir, file)
                    print(f"Moving {wav_filepath} to {dest_filepath}...")
                    shutil.move(wav_filepath, dest_filepath)

    root_dir = "./"
    convert_mp3_to_wav(root_dir)



def first_code():

    def windows(signal, window_size, step_size):
        if type(window_size) is not int:
            raise AttributeError("Window size must be an integer.")
        if type(step_size) is not int:
            raise AttributeError("Step size must be an integer.")
        for i_start in range(0, len(signal), step_size):
            i_end = i_start + window_size
            if i_end >= len(signal):
                break
            yield signal[i_start:i_end]

    def energy(samples):
        return np.sum(np.power(samples, 2.)) / float(len(samples))

    def rising_edges(binary_signal):
        previous_value = 0
        index = 0
        for x in binary_signal:
            if x and not previous_value:
                yield index
            previous_value = x
            index += 1


    def slicing(file_location, output_dir):
        '''
        Last Acceptable Values
        min_silence_length = 0.3
        silence_threshold = 1e-3
        step_duration = 0.03/10
        '''
        # Change the arguments and the input file here
        input_file = file_location
        output_dir = output_dir
        min_silence_length = 0.6  # The minimum length of silence at which a split may occur [seconds]. Defaults to 3 seconds.
        silence_threshold = 1e-4  # The energy level (between 0.0 and 1.0) below which the signal is regarded as silent.
        step_duration = min_silence_length/10   # The amount of time to step forward in the input file after calculating energy. Smaller value = slower, but more accurate silence detection. Larger value = faster, but might miss some split opportunities. Defaults to (min-silence-length / 10.).


        input_filename = input_file
        window_duration = min_silence_length
        if step_duration is None:
            step_duration = window_duration / 10.
        else:
            step_duration = step_duration

        output_filename_prefix = os.path.splitext(os.path.basename(input_filename))[0]

        sample_rate, samples = wavfile.read(filename=input_filename, mmap=True)

        max_amplitude = np.iinfo(samples.dtype).max
        print(max_amplitude)

        max_energy = energy([max_amplitude])
        print(max_energy)

        window_size = int(window_duration * sample_rate)
        step_size = int(step_duration * sample_rate)

        signal_windows = windows(
            signal=samples,
            window_size=window_size,
            step_size=step_size
        )

        window_energy = (energy(w) / max_energy for w in tqdm(
            signal_windows,
            total=int(len(samples) / float(step_size))
        ))

        window_silence = (e > silence_threshold for e in window_energy)

        cut_times = (r * step_duration for r in rising_edges(window_silence))

        cut_samples = [int(t * sample_rate) for t in cut_times]
        cut_samples.append(-1)

        cut_ranges = [(i, cut_samples[i], cut_samples[i+1]) for i in range(len(cut_samples) - 1)]

        for i, start, stop in tqdm(cut_ranges):
            if output_dir == './tmp/':
                output_file_path = "{}.wav".format(
                    os.path.join(output_dir, output_filename_prefix),
                )
            else:
                output_file_path = "{}_{:03d}.wav".format(
                    os.path.join(output_dir, output_filename_prefix),
                    i
                )

            print(f"Writing file {output_file_path}")
            wavfile.write(
                filename=output_file_path,
                rate=sample_rate,
                data=samples[start:stop]
            )


    def normalize_audio(audio_path, output):
        a = os.popen(f'ffmpeg -i {audio_path} -af "volumedetect" -f null /dev/null 2>&1 | findstr "max_volume"').read().lower() \
            .split('max_volume:')[1].split('db')[0]
        os.system(f'ffmpeg -i {audio_path} -af "volume={-float(a)}dB" {output}')


    def process_folders(parent_folder):
    # If there's any audio file with a length of 1 minute or less, exit the script
        if check_audio_length(parent_folder):
            print("An audio file with a length of 1 minute or less was found. Exiting...")
            time.sleep(1.5)
            return

        for root, dirs, files in os.walk(parent_folder):
            if 'wavs' in dirs:
                wav_folder = os.path.join(root, 'wavs')
                process_wav_folder(wav_folder, root)

    def check_audio_length(parent_folder):
        for root, dirs, files in os.walk(parent_folder):
            if 'wavs' in dirs:
                wav_folder = os.path.join(root, 'wavs')
                for wav_path in os.listdir(wav_folder):
                    if wav_path.endswith(".wav"):
                        wav_loc = os.path.join(wav_folder, wav_path)
                        with wave.open(wav_loc, 'rb') as wav_file:
                            n_frames = wav_file.getnframes()
                            frame_rate = wav_file.getframerate()
                            duration = n_frames / float(frame_rate)
                            if duration <= 60:
                                return True
        return False

    def process_wav_folder(wav_folder, parent_folder):
        for wav_path in os.listdir(wav_folder):
            if wav_path.endswith(".wav"):
                wav_loc = os.path.join(wav_folder, wav_path)
                process_wav_file(wav_loc, wav_folder, parent_folder)

    def process_wav_file(wav_loc, wav_folder, parent_folder):
        temp_folder = os.path.join(parent_folder, 'temp')
        rmtree(temp_folder, ignore_errors=True)
        os.makedirs(temp_folder, exist_ok=True)

        # Call slicing function and save the processed file in the temp_folder
        slicing(wav_loc, temp_folder)
        
        # Move the processed file(s) from temp_folder to the wav_folder
        for temp_wav_path in os.listdir(temp_folder):
            if temp_wav_path.endswith(".wav"):
                temp_wav_loc = os.path.join(temp_folder, temp_wav_path)
                shutil.move(temp_wav_loc, os.path.join(wav_folder, temp_wav_path))
        
        # Remove the original wav file
        os.remove(wav_loc)
        
        # Remove the temp folder
        if os.path.exists(temp_folder):
            shutil.rmtree(temp_folder)

    if __name__ == '__main__':
        parent_folder = "./"
        process_folders(parent_folder)
    pass


def second_code():

    parent_folder_path = './'

    sub_folders = [f.path for f in os.scandir(parent_folder_path) if f.is_dir()]

    for folder in sub_folders:
        wavs_folder_path = os.path.join(folder, 'wavs')
        wav_files = glob.glob(os.path.join(wavs_folder_path, '*.wav'))

        for index, wav_file in enumerate(wav_files, start=1):
            new_file_name = f"{index:04d}.wav"

            new_file_path = os.path.join(wavs_folder_path, new_file_name)

            shutil.move(wav_file, new_file_path)

            print(f"Renamed '{wav_file}' to '{new_file_path}'")


def third_code(language_code, model_name):

    model = whisper.load_model("large")
    lang_lst = [{language_code}]

    def process_wav_files(speaker_id, wav_folder, transcript_file, top_folder):
        with open(transcript_file, "w", encoding='utf-8') as f:
            for wav_file in sorted(os.listdir(wav_folder)):
                if wav_file.endswith(".wav"):
                    file_path = os.path.join(wav_folder, wav_file)
                    with open(file_path, "rb") as audio_file:
                        result = model.transcribe(file_path)

                    try:
                        detected_lang = detect(result['text'].strip())

                    except:

                        print(f"Files with different languages requested and recognized: {wav_file}, text: {result['text'].strip()}")
                        continue
                    
                    if (language_code == "ko" and detected_lang != "ko") or (language_code == "jp" and detected_lang != "jp") or (language_code == "en" and detected_lang != "en") or (language_code == "zh" and detected_lang != "zh"):
                        continue

                    else:
                        print(f"{wav_folder}/{wav_file}|{speaker_id}|{result['text'].strip()}")
                        f.writelines(f"{wav_folder}/{wav_file}|{speaker_id}|{result['text'].strip()}\n")
                        with open(os.path.join(top_folder, f"{model_name}_train.txt"), "a", encoding='utf-8') as all_transcript_file:
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
        
        input_file = f'./{model_name}_train.txt'
        output_file = f'./{model_name}_val.txt'

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

    main()


def fourth_code():
    top_folder_path = './'
    sub_folders = [f for f in os.listdir(top_folder_path) if os.path.isdir(os.path.join(top_folder_path, f))]

    output = ''
    output += ', '.join([f'"{folder}"' for folder in sub_folders])

    with open('speakers_list.txt', 'w', encoding='utf-8') as file:
        file.write(output.replace('\\"', '"'))


def fifth_code(model_name):
    f = open(f'./{model_name}_train.txt', 'r', encoding='utf-8').read().split('\n')

    l = []

    sec = 0
    for i in f:
        values = i.split('|')
        if len(values) != 3:
            print(f"Skipping line: {i}")
            continue

        p, speaker_id, t = values

        with contextlib.closing(wave.open(p, 'r')) as f:
            frames = f.getnframes()
            rate = f.getframerate()
            duration = frames / float(rate)
            sec += duration

    hours = int(sec // 3600)
    minutes = int((sec % 3600) // 60)
    print("Total datasets duration: {}hours {}minutes.".format(hours, minutes))


def create_config():
    config = {
    "train": {
        "log_interval": 200,
        "eval_interval": 1000,
        "seed": 1234,
        "epochs": 10000,
        "learning_rate": 2e-4,
        "betas": [0.8, 0.99],
        "eps": 1e-9,
        "batch_size": 32,
        "fp16_run": True,
        "lr_decay": 0.999875,
        "segment_size": 8192,
        "init_lr_ratio": 1,
        "warmup_epochs": 0,
        "c_mel": 45,
        "c_kl": 1.0
    },
    "data": {
        "training_files": "",
        "validation_files": "",
        "text_cleaners": [],
        "max_wav_value": 32768.0,
        "sampling_rate": 22050,
        "filter_length": 1024,
        "hop_length": 256,
        "win_length": 1024,
        "n_mel_channels": 80,
        "mel_fmin": 0.0,
        "mel_fmax": None,
        "add_blank": True,
        "n_speakers": 6,
        "cleaned_text": True
    },
    "model": {
        "inter_channels": 192,
        "hidden_channels": 192,
        "filter_channels": 768,
        "n_heads": 2,
        "n_layers": 6,
        "kernel_size": 3,
        "p_dropout": 0.1,
        "resblock": "1",
        "resblock_kernel_sizes": [3, 7, 11],
        "resblock_dilation_sizes": [[1, 3, 5], [1, 3, 5], [1, 3, 5]],
        "upsample_rates": [8, 8, 2, 2],
        "upsample_initial_channel": 512,
        "upsample_kernel_sizes": [16, 16, 4, 4],
        "n_layers_q": 3,
        "use_spectral_norm": False,
        "gin_channels": 256
    },
    "speakers": [],
    "symbols": [' japanese_symbols: "_", ",", ".", "!", "?", "-", "~", "\u2026", "A", "E", "I", "N", "O", "Q", "U", "a", "b", "d", "e", "f", "g", "h", "i", "j", "k", "m", "n", "o", "p", "r", "s", "t", "u", "v", "w", "y", "z", "\u0283", "\u02a7", "\u02a6", "\u2193", "\u2191", " " //korean_symbols: "_", ",", ".", "!", "?", "\u2026", "~", "\u3131", "\u3134", "\u3137", "\u3139", "\u3141", "\u3142", "\u3145", "\u3147", "\u3148", "\u314a", "\u314b", "\u314c", "\u314d", "\u314e", "\u3132", "\u3138", "\u3143", "\u3146", "\u3149", "\u314f", "\u3153", "\u3157", "\u315c", "\u3161", "\u3163", "\u3150", "\u3154", " " //en/zh_symbols: "_", ",", ".", "!", "?", "-", "~", "\u2026", "N", "Q", "a", "b", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "s", "t", "u", "v", "w", "x", "y", "z", "\u0251", "\u00e6", "\u0283", "\u0291", "\u00e7", "\u026f", "\u026a", "\u0254", "\u025b", "\u0279", "\u00f0", "\u0259", "\u026b", "\u0265", "\u0278", "\u028a", "\u027e", "\u0292", "\u03b8", "\u03b2", "\u014b", "\u0266", "\u207c", "\u02b0", "`", "^", "#", "*", "=", "\u02c8", "\u02cc", "\u2192", "\u2193", "\u2191", " " ']
}

    with open("config.json", "w", encoding="utf-8") as file:
        json.dump(config, file, ensure_ascii=False, indent=2)


def sixth_code(language_code, model_name):
    with open("config.json", "r", encoding="utf-8") as file:
        config = json.load(file)

    config["data"]["training_files"] = f"../{model_name}_datasets/{model_name}_train.txt.cleaned"
    config["data"]["validation_files"] = f"../{model_name}_datasets/{model_name}_val.txt.cleaned"

    wav_files = []
    for root, _, files in os.walk('.'):
        for file in files:
            if file.endswith('.wav'):
                wav_files.append(os.path.join(root, file))

    if wav_files:
        random_wav = random.choice(wav_files)
        with wave.open(random_wav, 'rb') as wav_file:
            sample_rate = wav_file.getframerate()

        config["data"]["sampling_rate"] = sample_rate

    with open("speakers_list.txt", "r", encoding="utf-8") as file:
        speakers = file.read().strip()

    speakers = [s.strip().strip('"') for s in speakers.split(',')]

    config["speakers"] = speakers

    with open("config.json", "w", encoding="utf-8") as file:
        json.dump(config, file, ensure_ascii=False, indent=2)

    if language_code == "ko":
        config["data"]["text_cleaners"] = ["korean_cleaners"]
    elif language_code == "ja":
        config["data"]["text_cleaners"] = ["japanese_cleaners2"]
    elif language_code == "en":
        config["data"]["text_cleaners"] = ["cjke_cleaners2"]
    elif language_code == "zh":
        config["data"]["text_cleaners"] = ["cjke_cleaners2"]

    subdirs = [d for d in os.listdir('.') if os.path.isdir(d)]
    config["data"]["n_speakers"] = len(subdirs)

    with open("config.json", "w", encoding="utf-8") as file:
        json.dump(config, file, ensure_ascii=False, indent=2)


def vits_preproess_code(language_code, model_name):
    import subprocess

    if language_code == "ko":
        text_cleaners = "korean_cleaners"
    elif language_code == "ja":
        text_cleaners = "japanese_cleaners2"
    elif language_code == "en":
        text_cleaners = "cjke_cleaners2"
    elif language_code == "zh":
        text_cleaners = "cjke_cleaners2"
    else:
        return
    
    script_path = "../vits/preprocess.py"

    text_index = "2"
    filelists_train = f'./{model_name}_train.txt'
    filelists_val = f'./{model_name}_val.txt'
    language_code = text_cleaners

    result = subprocess.run(["python", script_path, "--text_index", text_index, "--filelists", filelists_train, filelists_val, "--text_cleaners", language_code], capture_output=True, text=True)

    print("Return code:", result.returncode)
    print("stdout:", result.stdout)
    print("stderr:", result.stderr)


def rename_config_json(model_name):
    old_name = "config.json"
    new_name = f"{model_name}.json"

    if os.path.exists(old_name):
        os.rename(old_name, new_name)
        print(f"Renamed {old_name} to {new_name}")
    else:
        print(f"{old_name} not found")


def main():

    print("Running Audio Convertion(mp3 to wav, 44.1khz)")
    time.sleep(1.5)
    preprocessing_code(sys.argv[3])
    print("All .mp3 files have been converted to .wav files.\n")

    print("Running Audio Seperation...")
    time.sleep(1.5)
    first_code()
    print("All .wav files have been seperated.\n")

    print("Running Audio Files Rename...")
    time.sleep(1.5)
    second_code()
    print("All .wav files have been renamed.\n")

    print("Running Whisper ASR...")
    time.sleep(0.5)
    third_code(sys.argv[1], sys.argv[2])
    print("All .wav files have been processed.\n")

    print("Running vits preprocess.py...")
    time.sleep(1.5)
    vits_preproess_code(sys.argv[1], sys.argv[2])
    print("The cleaner has successfully processed the text file.\n")

    print("Creating Speakers ID...")
    time.sleep(1.5)
    fourth_code()
    print("Successfully created speaker ID.\n")

    print("Creating config.json...")
    time.sleep(1.5)
    create_config()
    print("Successfully created config.json.\n")

    print("Editing config.json...")
    time.sleep(1.5)
    sixth_code(sys.argv[1], sys.argv[2])
    print("Successfully edited config.json.\n")

    print("Renaming config.json...")
    time.sleep(1.5)
    rename_config_json(sys.argv[2])
    print("Successfully renamed config.json.\n")

    print("Measuring Total Datasets Duration...")
    time.sleep(1.5)
    fifth_code(sys.argv[2])
    print("Successfully measured dataset length.\n")

    print("All codes have been executed successfully.")


if __name__ == "__main__":
    main()
