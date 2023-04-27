import os

folder_path = "../minami/wavs"

for filename in os.listdir(folder_path):
    if filename.endswith(".wav"):
        file_path = os.path.join(folder_path, filename)
        if os.path.getsize(file_path) < 100000:
            os.remove(file_path)
            print(f"{filename} deleted.")