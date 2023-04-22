from scipy.io import wavfile
import os
import numpy as np
from tqdm import tqdm
from shutil import rmtree
import sys

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


if __name__ == '__main__':

    

    # wav_loc = sys.argv[1]

    for wav_path in os.listdir('wavs'):

        rmtree('./sliced/', ignore_errors=True)
        rmtree('./rev/', ignore_errors=True)
        rmtree('./tmp/', ignore_errors=True)
        rmtree('./unnormalize/', ignore_errors=True)

        os.makedirs('sliced', exist_ok=True)
        os.makedirs('rev', exist_ok=True)
        os.makedirs('tmp', exist_ok=True)
        os.makedirs('unnormalize', exist_ok=True)
        os.makedirs('result', exist_ok=True)

        wav_loc = f'wavs\\{wav_path}'

        slicing(wav_loc, './sliced/')

        os.system('FOR /F "tokens=*" %G IN (\'dir /b sliced\\*.wav\') DO ffmpeg -y -i "sliced\\%G" -vf reverse -af areverse "./rev/%~nG.wav" ')

        rev_wav_lst = [i for i in os.listdir('./rev/') if i.endswith('.wav')]

        for rwl in rev_wav_lst:
            slicing(f'./rev/{rwl}', './tmp/')

        os.system('FOR /F "tokens=*" %G IN (\'dir /b tmp\\*.wav\') DO ffmpeg -y -i "tmp\\%G" -vf reverse -af areverse "./unnormalize/%~nG.wav" ')
        
        unnormalize_wav_lst = [i for i in os.listdir('./unnormalize/') if i.endswith('.wav')]
        for uwl in unnormalize_wav_lst:
            normalize_audio(f'./unnormalize/{uwl}', f'./result/{uwl}')
        
