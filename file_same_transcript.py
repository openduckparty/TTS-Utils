import os
import json

path = os.path.abspath('./wavs')
d = os.listdir(path)

t = {}

for i in d:
    if i.endswith('.wav'):
        p = os.path.abspath(i)
        transcript = i.split('.wav')[0]
        t[p] = transcript

with open("mb_transcription.json", "w", encoding='utf-8') as outfile:
    json.dump(t, outfile, indent=4, sort_keys=False, ensure_ascii=False)
