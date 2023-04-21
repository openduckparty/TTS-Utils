import random

def select_random_lines(input_file, output_file, total_lines, lines_to_select):
    with open(input_file, 'r', encoding='utf-8') as file:
        all_lines = file.readlines()
    
    selected_lines = random.sample(all_lines, lines_to_select)

    with open(output_file, 'w', encoding='utf-8') as file:
        for line in selected_lines:
            file.write(line)

input_file = './blueac.txt'  # 원본 메모장 파일 경로
output_file = './output.txt'  # 결과를 저장할 메모장 파일 경로
total_lines = 9324  # 원본 메모장의 전체 줄 수
lines_to_select = 93  # 선택할 줄 수

select_random_lines(input_file, output_file, total_lines, lines_to_select)
