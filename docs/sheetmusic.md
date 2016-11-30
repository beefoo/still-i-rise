# Sheet music generation

Starting from an audio file of speech, generate sheet music

## Requirements

All software used is free and/or open-source

* [Python](https://www.python.org/) - for various data processing
* [Lilypond](http://lilypond.org/) - for sheet music engraving

## Analyze speech

Follow the steps outlined in [this document](speech_analysis.md) to generate speech data.

### Generate lilypond file

This will generate a lilypond (.ly) file based on the speech data

```
python sheet_music.py
```

### Generate sheet music

Open generated .ly file from previous step in [Lilypond](http://lilypond.org/)
