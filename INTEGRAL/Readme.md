##DATA PREPARING

.mp3 or .wav files are okay.

```
INTEGRAL
├───speaker0
│   ├────1.mp3
│   └────1.wav
└───speaker1
    ├───1.mp3
    └───1.wav
INTEGRAL.py
```

##RUN

python INTEGRAL.py <speaker's target language> <your model name> <wanted_sample_rate>

After you have finished running INTEGRAL.py, please open config.json and you have to edit.
    
    INTEGRAL.py, Line 400, "symbols": [' japanese_symbols: ... //korean_symbols: ... //en/zh_symbols: ... ']
    
Please delete everything except the language symbol you want. Please remove the first part of "(your_language)_symbols:" and the small quotation marks on the first and last sentences.

and VITS Training!
    
