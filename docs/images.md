# Speech visualizations

Starting from an audio file of speech, generate speech visualizations

## Requirements

All software used is free and/or open-source

* [FFmpeg](https://www.ffmpeg.org/) - for media processing
* [Praat](http://www.fon.hum.uva.nl/praat/) - for speech analysis
* [Python](https://www.python.org/) - for various data processing

## Analyze speech

Follow the steps outlined in [this document](speech_analysis.md) to generate speech data.

## Generate visualizations

1. Generate Praat TextGrid files

  ```
  python lines_to_textgrids.py
  ```

2. Generate audio clips

  ```
  python generate_clips.py
  ```

3. Generate an .eps sound viz file of audio clip

  ```
  python draw_sound.py -sf clips/lines/line_000_1.wav -tf textgrids/line_000_1.TextGrid -out data/line_000_1.eps
  ```
