input_file_path = './transcript.txt'
with open(input_file_path, 'r', encoding='utf-8') as file:
    lines = file.readlines()

sorted_lines = sorted(lines, key=lambda x: int(x.split('|')[0].split('/')[-1].split('.')[0]))

output_file_path = './file.txt'
with open(output_file_path, 'w', encoding='utf-8') as file:
    file.writelines(sorted_lines)

print(f"Successfully sorted and saved to {output_file_path}")
