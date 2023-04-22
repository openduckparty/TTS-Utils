import os

# 상위 폴더 경로를 지정하세요.
top_folder_path = './'

# 상위 폴더 내의 하위 폴더 목록을 가져옵니다.
sub_folders = [f for f in os.listdir(top_folder_path) if os.path.isdir(os.path.join(top_folder_path, f))]

# 메모장에 저장할 문자열을 만듭니다.
output = 'speakers: [\n    '
output += ', '.join([f'"{folder}"' for folder in sub_folders])
output += '\n]'

# 메모장 파일에 문자열을 저장합니다.
with open('speakers_list.txt', 'w', encoding='utf-8') as file:
    file.write(output)

print("작성 완료!")
