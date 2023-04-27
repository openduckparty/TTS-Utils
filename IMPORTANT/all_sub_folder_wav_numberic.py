import os
import glob
import shutil

# 상위 폴더 경로
parent_folder_path = './'

# 상위 폴더 아래의 하위 폴더 목록을 얻습니다.
sub_folders = [f.path for f in os.scandir(parent_folder_path) if f.is_dir()]

# 하위 폴더들을 반복합니다.
for folder in sub_folders:
    # 각 하위 폴더의 wavs 폴더 경로를 생성합니다.
    wavs_folder_path = os.path.join(folder, 'wavs')

    # wavs 폴더 내의 .wav 파일 목록을 얻습니다.
    wav_files = glob.glob(os.path.join(wavs_folder_path, '*.ogg'))

    # .wav 파일들을 반복하면서 이름을 변경합니다.
    for index, wav_file in enumerate(wav_files, start=1):
        # 새 파일 이름을 생성합니다 (예: 0001.wav, 0002.wav, ...)
        new_file_name = f"{index:04d}.ogg"

        # 새 파일 경로를 생성합니다.
        new_file_path = os.path.join(wavs_folder_path, new_file_name)

        # 파일 이름을 변경합니다.
        shutil.move(wav_file, new_file_path)

        print(f"Renamed '{wav_file}' to '{new_file_path}'")