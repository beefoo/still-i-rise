# Speech analysis

Starting from an audio file of speech, generate speech and sound data

## Requirements

All software used is free and/or open-source

* [FFmpeg](https://www.ffmpeg.org/) - for media processing
* [Praat](http://www.fon.hum.uva.nl/praat/) - for speech analysis
* [Gentle](https://github.com/lowerquality/gentle) - for transcript alignment to audio
* [Python](https://www.python.org/) - for various data processing

## Pre-Process audio

This step creates the .wav file from source .mp4 file

1. Download .mp4 file of video
2. [Clip video](https://trac.ffmpeg.org/wiki/Seeking#Cuttingsmallsections) if necessary

   ```
   ffmpeg -i still_i_rise_original.mp4 -ss 42.0 -c copy still_i_rise.mp4
   ```

   This removes the first 42 seconds of the file

3. [Extract .wav](http://superuser.com/a/791874) audio file:

   ```
   ffmpeg -i still_i_rise.mp4 -vn -acodec pcm_s16le -ar 44100 -ac 2 still_i_rise.wav
   ```

## Extract speech data

This step extracts amplitude, pitch, and voice pulse data from .wav file using [Praat](http://www.fon.hum.uva.nl/praat/)

1. Download [Praat](http://www.fon.hum.uva.nl/praat/) and add the Praat directory to your PATH so you can execute Praat from the command line
2. Run script to collect pitch, intensity, and voice pulse data

  ```
  python collect_sound_data.py
  ```

3. The above script will generate .Pitch and .PointProcess short text files

You can also do the above steps manually in Praat's GUI:

1. Open .wav file in Praat
2. Click **View & Edit**
3. Show analysis by clicking **View** -> **Show Analysis...** -> **Longest Analysis** -> 200 -> Apply
4. Click **Pitch** and update settings (adjust as needed):
  * Pitch range: *75 - 256*
  * Advanced settings: Check *very accurate*
  * Silence threshold: *0.02*
  * Voicing threshold: *0.3*
  * Octave cost: *0.001*
  * Octave-jump cost: *0.3*
5. Apply and Okay; Click **Pitch** -> **Extract visible pitch contour**
6. Go to objects window, select Pitch object, and **Save** -> **short text file** (e.g. still_i_rise.Pitch) - this will be your pitch data
7. Click **Pulses** -> **Show Pulses**
8. Click **Pulses** -> **Extract visible pulses**
9. Go to objects window, select PointProcess object, and **Save** -> **short text file** (e.g. still_i_rise.PointProcess) - this will be your voice pulse data

### Align transcript to audio

1. Download, install, and run [Gentle](https://github.com/lowerquality/gentle)
2. Use GUI to align .wav file and .txt file via `http://localhost:8765/`
3. Save aligned .json file
4. Clean up timings:

  ```
  python clean.py
  ```

4. Add verses and lines:

  ```
  python add_lines.py
  ```

### Find non-words and pauses

```
python find_nonwords.py
```

### Generate syllables

1. Install [NLTK](http://www.nltk.org/) for Python:

  ```
  sudo pip install -U nltk
  ```

2. Download cmudict corpus:

  ```
  sudo python -m nltk.downloader -d /usr/local/share/nltk_data cmudict
  ```

3. Run script:

  ```
  python find_syllables.py
  ```

### Analyze sound for pitch and frequency data

```
python analyze_sound.py
```
