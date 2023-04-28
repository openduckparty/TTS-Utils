#sys.argv[1] = ex) ko, ja, en, zh
#sys.argv[2] = ex) korean, japanese, english, chinese
#sys.argv[3] = ALL transcription saved in this txt. insert model name

import os
import glob
import shutil
import numpy as np
import random
import whisper
import sys
import time
import os
import wave
import contextlib
from tqdm import tqdm
from shutil import rmtree
from scipy.io import wavfile

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
        for root, dirs, files in os.walk(parent_folder):
            if 'wavs' in dirs:
                wav_folder = os.path.join(root, 'wavs')
                process_wav_folder(wav_folder, root)

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


def third_code(arg1, arg2, arg3):

    model = whisper.load_model("large")
    lang_lst = [{arg1}, {arg2}]

    def process_wav_files(speaker_id, wav_folder, transcript_file, top_folder):
        with open(transcript_file, "w", encoding='utf-8') as f:
            for wav_file in sorted(os.listdir(wav_folder)):
                if wav_file.endswith(".wav"):
                    file_path = os.path.join(wav_folder, wav_file)
                    with open(file_path, "rb") as audio_file:
                        result = model.transcribe(file_path)
                    print(f"{wav_folder}/{wav_file}|{speaker_id}|{result['text'].strip()}")
                    f.writelines(f"{wav_folder}/{wav_file}|{speaker_id}|{result['text'].strip()}\n")
                    with open(os.path.join(top_folder, f"{arg3}_train.txt"), "a", encoding='utf-8') as all_transcript_file:
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
        
        input_file = f'./{arg3}_train.txt'
        output_file = f'./{arg3}_val.txt'

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

    output = 'speakers: [\n    '
    output += ', '.join([f'"{folder}"' for folder in sub_folders])
    output += '\n]'

    with open('speakers_list.txt', 'w', encoding='utf-8') as file:
        file.write(output)

    print("Completed!")


def fifth_code(arg3):
    f = open(f'./{arg3}_train.txt', 'r', encoding='utf-8').read().split('\n')

    l = []

    c = 0
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
            c += duration

    print('Total Datasets Duration = ', c)


def main():

    print("Running Audio Seperation...")
    time.sleep(1.5)
    first_code()

    print("Running Audio Files Rename...")
    time.sleep(1.5)
    second_code()

    print("Running Whisper ASR...")
    time.sleep(1.5)
    third_code(sys.argv[1], sys.argv[2], sys.argv[3])

    print("Running Create Speakers ID...")
    time.sleep(1.5)
    fourth_code()

    print("Running Total Datasets Duration...")
    time.sleep(1.5)
    fifth_code()

    print("All codes have been executed successfully")


if __name__ == "__main__":
    main()
