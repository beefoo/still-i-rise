# Still I Rise: A Close Listening

A deep analysis of Maya Angelou's performance of _Still I Rise_

## Requirements

* [FFmpeg](https://www.ffmpeg.org/) - for media processing
* [Praat](http://www.fon.hum.uva.nl/praat/) - for speech analysis
* [ChucK](http://chuck.cs.princeton.edu/) - for audio construction
* [Gentle](https://github.com/lowerquality/gentle) - for transcript alignment to audio
* [Python](https://www.python.org/) - for various data processing

## Processing a media file from scratch

This is just self-documentation for how I went from a media file to final product

### Pre-Process audio

This step creates the .wav file from source .mp4 file

1. Download .mp4 file of video
2. [Clip video](https://trac.ffmpeg.org/wiki/Seeking#Cuttingsmallsections) if necessary

   ```
   ffmpeg -i and_still_i_rise_original.mp4 -ss 42.0 -c copy and_still_i_rise.mp4
   ```

3. [Extract .wav](http://superuser.com/a/791874) audio file:

   ```
   ffmpeg -i and_still_i_rise.mp4 -vn -acodec pcm_s16le -ar 44100 -ac 2 and_still_i_rise.wav
   ```

### Extract speech data

This step extracts amplitude, pitch, and voice pulse data from .wav file using [Praat](http://www.fon.hum.uva.nl/praat/)

1. Open .wav file in [Praat](http://www.fon.hum.uva.nl/praat/)
2. _(optional)_ Select object, then click **Save** -> **short text file** (e.g. and_still_i_rise.Sound) - this will give you raw amplitude data
2. Click **View & Edit**
3. Show analysis by clicking **View** -> **Show Analysis...** -> **Longest Analysis** -> 200 -> Apply
4. Click **Pitch** and update settings (adjust as needed):
  * Pitch range: *80 - 180*
  * Advanced settings: Check *very accurate*
  * Silence threshold: *0.03*
  * Voicing threshold: *0.3*
  * Octave cost: *0.001*
  * Octave-jump cost: *0.3*
5. Apply and Okay; Click **Pitch** -> **Extract visible pitch contour**
6. Go to objects window, select Pitch object, and **Save** -> **short text file** (e.g. and_still_i_rise.Pitch) - this will be your pitch data
7. Click **Pulses** -> **Show Pulses**
8. Click **Pulses** -> **Extract visible pulses**
9. Go to objects window, select PointProcess object, and **Save** -> **short text file** (e.g. and_still_i_rise.PointProcess) - this will be your voice pulse data

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

### Add pitch (frequency) and volume (intensity) data

```
python add_sound_data.py
```

### Extract words, syllables, nonwords, pauses from audio

```
python generate_clips.py
```

Uses subprocesses to run commands like this:

```
ffmpeg -i and_still_i_rise.wav -ss 2.83 -to 3.58 -c copy words/history.wav
```

### Process frames

1. Convert .mp4 to .jpg frames (15fps)

  ```
  ffmpeg -i and_still_i_rise.mp4 -r 15/1 frames/frame%04d.jpg
  ```

2. Convert .jpg frames (15fps) to .mp4 (15fps) ([ref](https://trac.ffmpeg.org/wiki/Create%20a%20video%20slideshow%20from%20images))

  ```
  ffmpeg -framerate 15/1 -i frames/frame%04d.jpg -c:v libx264 -r 15 -pix_fmt yuv420p output/and_still_i_rise.mp4
  ```
