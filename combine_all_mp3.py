import os
from pydub import AudioSegment

def combine_mp3_files(folder_path, output_file):
    mp3_files = [file for file in os.listdir(folder_path) if file.endswith('.mp3')]
    combined = AudioSegment.empty()

    for mp3_file in mp3_files:
        mp3_path = os.path.join(folder_path, mp3_file)
        audio_segment = AudioSegment.from_mp3(mp3_path)
        combined += audio_segment

    combined.export(output_file, format='mp3')

folder_path = './'
output_file = 'combined_output.mp3'

combine_mp3_files(folder_path, output_file)
