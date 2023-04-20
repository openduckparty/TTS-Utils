import os

folder_path = './wavs' # Replace with the path to your folder
count = 1

for filename in os.listdir(folder_path):
    if filename.endswith('.wav'):
        new_filename = str(count).zfill(4) + '.wav' # Renames files with leading zeros for sorting purposes
        os.rename(os.path.join(folder_path, filename), os.path.join(folder_path, new_filename))
        count += 1