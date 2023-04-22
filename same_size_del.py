import os
import glob

# Specify the folder path containing the .wav files
folder_path = '../minami/wavs'

# Get a list of all .wav files in the specified folder
wav_files = glob.glob(os.path.join(folder_path, '*.wav'))

# Create a dictionary to store unique file sizes and their file paths
file_sizes = {}

# Iterate through each .wav file
for file in wav_files:
    # Get the file size
    file_size = os.path.getsize(file)

    # If the file size is not in the dictionary, add it with the file path
    if file_size not in file_sizes:
        file_sizes[file_size] = file
    # If the file size is already in the dictionary, delete the duplicate file
    else:
        os.remove(file)

print("Duplicate files with the same size have been deleted.")
