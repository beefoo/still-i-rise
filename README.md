# And Still I Rise

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
   ffmpeg -i and_still_i_rise_original.mp4 -ss 42.0  -c copy and_still_i_rise.mp4
   ```

3. [Extract .wav](http://superuser.com/a/791874) audio file:

   ```
   ffmpeg -i and_still_i_rise.mp4 -vn -acodec pcm_s16le -ar 44100 -ac 2 and_still_i_rise.wav
   ```

### Extract speech data

This step extracts amplitude, pitch, and voice pulse data from .wav file using [Praat](http://www.fon.hum.uva.nl/praat/)

1. Open .wav file in [Praat](http://www.fon.hum.uva.nl/praat/)
2. Select object, then click **Save** -> **short text file** (e.g. and_still_i_rise.Sound) - this will be your amplitude data
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
