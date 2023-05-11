DATA PREPARING
===============

.mp3 or .wav files are okay.

```
INTEGRAL
├───speaker0
│   ├────1.mp3
│   └────1.wav
└───speaker1
│    ├───1.mp3
│    └───1.wav
└INTEGRAL.py
```

RUN
=============

    python INTEGRAL.py <speaker's target language> <your model name> <wanted_sample_rate>

After you have finished running INTEGRAL.py, please open config.json and you have to edit.

    "symbols": []
    
Please refer to the .json file in the VITS/config folder and modify the symbols part.

and VITS Training!
    
