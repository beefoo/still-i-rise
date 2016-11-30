# Midi generation

Starting from an audio file of speech, generate a midi file

## Requirements

All software used is free and/or open-source

* [FFmpeg](https://www.ffmpeg.org/) - for media processing
* [Python](https://www.python.org/) - for various data processing
* [Fluidsynth](http://www.fluidsynth.org/) with [libsndfile](https://github.com/erikd/libsndfile) - for midi-to-wav conversion
* [Fluid R3 GM Soundfont](https://musescore.org/en/handbook/soundfont#list) or equivalent - for midi playback/processing

## Analyze speech

Follow the steps outlined in [this document](speech_analysis.md) to generate speech data.

## Generate midi file

```
python midi.py
```

## Generate wav file

```
fluidsynth -F still_i_rise_midi.wav fluidr3gm.sf2 data/still_i_rise.mid
```

## Mix the original audio w/ the midi audio

```
ffmpeg -i still_i_rise_midi.wav -i still_i_rise.wav -filter_complex "[0:a][1:a]amerge,pan=stereo|c0<c0+c1|c1<c2+c3[aout]" -map "[aout]" -shortest still_i_rise_mixed.wav
```
