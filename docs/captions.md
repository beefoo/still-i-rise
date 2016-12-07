# Captioned video generation

Starting from an video file of speech, generate a video with captions

## Requirements

All software used is free and/or open-source

* [Python](https://www.python.org/) - for various data processing
* [FFmpeg](https://www.ffmpeg.org/) - for media processing
* [Processing](http://processing.org/) - for image processing

## Analyze speech

Follow the steps outlined in [this document](speech_analysis.md) (up until `4. Add verses and lines:` step) to generate speech data.

## Generate frames

1. Convert .mp4 to .png frames (15fps)

  ```
  ffmpeg -i still_i_rise.mp4 -r 15/1 -q:v 1 frames/frame%04d.png
  ```

2. Open up and run `./caption/caption.pde` in Processing. This will generate frames to `./caption/output/frames`

3. Compile the frames to .mp4

  ```
  ffmpeg -framerate 15/1 -i caption/output/frames/frame%04d.png -c:v libx264 -r 15 -pix_fmt yuv420p -q:v 1 caption/output/stil_i_rise_compiled.mp4
  ```

4. Add audio track

  ```
  ffmpeg -i caption/output/stil_i_rise_compiled.mp4 -i still_i_rise.wav -c:v libx264 -c:a libfaac -shortest stil_i_rise_captioned.mp4
  ```
