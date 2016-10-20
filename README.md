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
