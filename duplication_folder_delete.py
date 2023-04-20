import os
import shutil

# 상위 폴더의 경로를 지정합니다.
parent_folder_path = './'

# 상위 폴더의 모든 하위 폴더를 순회합니다.
for folder_name in os.listdir(parent_folder_path):
    subfolder_path = os.path.join(parent_folder_path, folder_name)

    # 하위 폴더가 디렉토리인지 확인합니다.
    if os.path.isdir(subfolder_path):
        wavs_folder_path = os.path.join(subfolder_path, 'wavs')

        # wavs 폴더가 있는지 확인하고 삭제합니다.
        if os.path.exists(wavs_folder_path) and os.path.isdir(wavs_folder_path):
            shutil.rmtree(wavs_folder_path)
            print(f'"{wavs_folder_path}" 폴더가 삭제되었습니다.')
