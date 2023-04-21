import random

def select_random_lines(input_file, output_file, total_lines, lines_to_select):
    with open(input_file, 'r', encoding='utf-8') as file:
        all_lines = file.readlines()
    
    selected_lines = random.sample(all_lines, lines_to_select)

    with open(output_file, 'w', encoding='utf-8') as file:
        for line in selected_lines:
            file.write(line)

input_file = './blueac.txt'
output_file = './output.txt'
total_lines = 9324
lines_to_select = 93

select_random_lines(input_file, output_file, total_lines, lines_to_select)
