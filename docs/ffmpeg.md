[Trim first 5s from beginning of video](https://trac.ffmpeg.org/wiki/Seeking#Cuttingsmallsections)

```
ffmpeg -i in.mp4 -ss 5.0 -c copy out.mp4
```

Clip video from 5s to 10s

```
ffmpeg -i in.mp4 -ss 5.0 -to 10.0 -c copy out.mp4
```

[Extract .wav](http://superuser.com/a/791874) from .mp4:

 ```
 ffmpeg -i in.mp4 -vn -acodec pcm_s16le -ar 44100 -ac 2 out.wav
 ```

[Convert .mov to .mp4](http://stackoverflow.com/questions/12026381/ffmpeg-converting-mov-files-to-mp4)

```
ffmpeg -i input.mov -qscale 0 output.mp4
```

Clip audio file from 5s to 10s, then add fade in/out in the first/last 0.5s

```
ffmpeg -i in.wav -ss 5.0 -to 10.0 -c copy temp.wav -y
ffmpeg -i temp.wav -af 'afade=t=in:ss=0:d=0.5,afade=t=out:st=4.5:d=0.5' out.wav -y
rm temp.wav
```

Convert .mp4 to .png frames (15fps)

```
ffmpeg -i in.mp4 -r 15/1 -q:v 1 frames/frame%04d.png
```

[Convert .png frames (15fps) to .mp4 (15fps)](https://trac.ffmpeg.org/wiki/Create%20a%20video%20slideshow%20from%20images)

```
ffmpeg -framerate 15/1 -i frames/frame%04d.png -c:v libx264 -r 15 -pix_fmt yuv420p -q:v 1 out.mp4
```

[Add audio to video](http://stackoverflow.com/questions/11779490/how-to-add-a-new-audio-not-mixing-into-a-video-using-ffmpeg)

```
ffmpeg -i in.mp4 -i in.wav -c:v libx264 -c:a libfaac -shortest out.mp4
```

Duration will be the shortest of the two files
