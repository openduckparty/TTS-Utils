import os
import shutil

# 상위 폴더 경로 설정
parent_dir = './'

# 상위 폴더의 모든 하위 폴더 가져오기
subdirectories = [d for d in os.listdir(parent_dir) if os.path.isdir(os.path.join(parent_dir, d))]

# 각 하위 폴더에서 작업 수행
for subdir in subdirectories:
    subdir_path = os.path.join(parent_dir, subdir)
    
    # 하위 폴더의 모든 파일과 폴더 가져오기
    all_files = os.listdir(subdir_path)
    
    # ./wav 폴더 생성 (이미 존재하는 경우 에러 방지)
    wav_dir = os.path.join(subdir_path, 'wavs')
    if not os.path.exists(wav_dir):
        os.makedirs(wav_dir)

    # 하위 폴더의 모든 .wav 파일을 ./wav 폴더로 옮기기
    for file in all_files:
        if file.endswith('.ogg'):
            src = os.path.join(subdir_path, file)
            dst = os.path.join(wav_dir, file)
            shutil.move(src, dst)
