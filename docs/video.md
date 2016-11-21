# Video generation

## Requirements

All software used is free and/or open-source

* [FFmpeg](https://www.ffmpeg.org/) - for media processing
* [OpenCV](http://opencv.org/) - for image processing and analysis
* [Python](https://www.python.org/) - for various data processing

## Analyze frames

### Install Open CV

```
brew tap homebrew/science
brew install opencv3 --with-contrib
cd /Library/Python/2.7/site-packages/
ln -s /usr/local/Cellar/opencv3/3.1.0_4/lib/python2.7/site-packages/cv2.so cv2.so
```

And install numpy

```
pip install numpy
```

### Detect edge

```
python detect_edge.py
```

### Detect flow

```
python detect_flow.py
```

## Process frames

1. Convert .mp4 to .png frames (15fps)

  ```
  ffmpeg -i still_i_rise.mp4 -r 15/1 -q:v 1 frames/frame%04d.png
  ```

2. Convert .png frames (15fps) to .mp4 (15fps) ([ref](https://trac.ffmpeg.org/wiki/Create%20a%20video%20slideshow%20from%20images))

  ```
  ffmpeg -framerate 15/1 -i frames/frame%04d.png -c:v libx264 -r 15 -pix_fmt yuv420p -q:v 1 output/still_i_rise.mp4
  ```
