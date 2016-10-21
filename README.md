# And Still I Rise

## Requirements

* [FFmpeg](https://www.ffmpeg.org/) - for media processing
* [Praat](http://www.fon.hum.uva.nl/praat/) - for speech analysis
* [ChucK](http://chuck.cs.princeton.edu/) - for audio construction
* [Python](https://www.python.org/) - for various data processing

## Process

1. Download .mp4 file of [video](https://www.youtube.com/watch?v=JqOqo50LSZ0)
2. [Clip video](https://trac.ffmpeg.org/wiki/Seeking#Cuttingsmallsections) to just include poem:

   ```
   ffmpeg -i and_still_i_rise_original.mp4 -ss 42.0  -c copy and_still_i_rise.mp4
   ```

3. [Extract .wav](http://superuser.com/a/791874) audio file:

   ```
   ffmpeg -i and_still_i_rise.mp4 -vn -acodec pcm_s16le -ar 44100 -ac 2 and_still_i_rise.wav
   ```

4. Extract speech data using [Praat](http://www.fon.hum.uva.nl/praat/)
   1. Open .wav file
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
   9. Go to objects window, select PointProcess object, and **Save** -> **short text file** (e.g. and_still_i_rise.PointProcess) - this will be your pulse data
