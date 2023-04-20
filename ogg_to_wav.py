import os
import subprocess
import shutil

# 상위 폴더 내 모든 하위 폴더를 탐색
for subdir, dirs, _ in os.walk('.'):
    # 'wavs' 폴더를 찾으면 처리 시작
    if 'wavs' in dirs:
        wavs_path = os.path.join(subdir, 'wavs')
        converted_wavs_path = os.path.join(subdir, 'converted_wavs')

        # 'converted_wavs' 폴더 생성
        if not os.path.exists(converted_wavs_path):
            os.makedirs(converted_wavs_path)

        # 'wavs' 폴더 내의 .ogg 파일을 처리
        for file in os.listdir(wavs_path):
            if file.endswith('.ogg'):
                input_file = os.path.join(wavs_path, file)
                output_file = os.path.join(converted_wavs_path, f"{os.path.splitext(file)[0]}.wav")

                # ffmpeg를 사용하여 .ogg 파일을 .wav 파일로 변환 (샘플 레이트: 44100hz)
                subprocess.run(['ffmpeg', '-i', input_file, '-ar', '44100', output_file])

        shutil.rmtree(wavs_path)  # 추가
        