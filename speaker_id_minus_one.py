with open('transcript.txt', 'r', encoding='utf-8') as infile:
    lines = infile.readlines()

with open('modified_transcript.txt', 'w', encoding='utf-8') as outfile:
    for line in lines:
        path, speaker_id, transcript = line.strip().split('|')
        new_speaker_id = int(speaker_id) - 1
        new_line = f"{path}|{new_speaker_id}|{transcript}\n"
        outfile.write(new_line)
