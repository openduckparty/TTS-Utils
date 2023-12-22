# Read lines from the input file
input_file_path = './transcript.txt'
with open(input_file_path, 'r', encoding='utf-8') as file:
    lines = file.readlines()

# Extract and sort lines based on the numeric part
sorted_lines = sorted(lines, key=lambda x: int(x.split('|')[0].split('/')[-1].split('.')[0]))

# Write sorted lines to a new file
output_file_path = './file.txt'
with open(output_file_path, 'w', encoding='utf-8') as file:
    file.writelines(sorted_lines)

print(f"File successfully sorted and saved to {output_file_path}")
