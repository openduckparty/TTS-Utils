input_file_path = './jsut_train.txt'
output_file_path = './jsut_train2.txt'

with open(output_file_path, 'w', encoding='utf-8') as output_file:
    for speaker_id in range(71):
        with open(input_file_path, 'r', encoding='utf-8') as input_file:
            lines = input_file.readlines()

            for line in lines:
                new_line = line.replace('|0|', f'|{speaker_id}|')
                output_file.write(new_line)

            if speaker_id < 70:
                output_file.write('\n')

print("뻥튀기 완료!")
