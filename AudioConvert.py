import os
from pydub import AudioSegment

# Set the path to the folder containing the MP3 files
folder_path = "C:/Users/whals/Desktop/dahye/mp3"

# Loop through all the files in the folder
for filename in os.listdir(folder_path):
    # Check if the file is an MP3 file
    if filename.endswith(".mp3"):
        # Load the MP3 file
        sound = AudioSegment.from_file(os.path.join(folder_path, filename), format="mp3")

        # Set the sample rate to 22050Hz and convert to mono
        sound = sound.set_frame_rate(44100).set_channels(1)

        # Save the file as WAV
        output_filename = os.path.splitext(filename)[0] + ".wav"
        output_path = os.path.join(folder_path, output_filename)
        sound.export(output_path, format="wav")