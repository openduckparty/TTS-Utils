import os
import shutil

# 상위 폴더 경로를 지정해주세요.
top_folder_path = './'

# 상위 폴더 내의 모든 하위폴더를 가져옵니다.
sub_folders = [os.path.join(top_folder_path, folder) for folder in os.listdir(top_folder_path)]

# 각 하위 폴더 내의 'wavs' 폴더에 있는 .spec.pt 파일들을 삭제합니다.
for sub_folder in sub_folders:
    wavs_folder = os.path.join(sub_folder, 'wavs')
    
    # 'wavs' 폴더가 존재할 경우 .spec.pt 파일들을 찾아 삭제합니다.
    if os.path.exists(wavs_folder):
        files_to_delete = [file for file in os.listdir(wavs_folder) if file.endswith('.spec.pt')]
        
        for file in files_to_delete:
            file_path = os.path.join(wavs_folder, file)
            os.remove(file_path)
            print(f'{file_path} 파일이 삭제되었습니다.')

print('모든 .spec.pt 파일이 삭제되었습니다.')
