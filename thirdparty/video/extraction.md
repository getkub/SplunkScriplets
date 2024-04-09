## Extract videos using yt-dlp

- Download `yt-dlp` and move it to `/usr/local/bin/`
- brew install ffmpeg

```
vid="sFJyYLqNK8M"
url="https://www.youtube.com/watch?v=${vid}"
yt-dlp "${url}" -o ${vid}.webm

# Put times and duration to extract etc
# For 1hr:21min:34s, the time is 4894 and for duration of 10seconds
sss="4894"
dur="10"

# Audio
ffmpeg -ss ${sss} -t ${dur} -i ${vid}.webm -y -vn -acodec copy audio-${vid}.mp3

# Video
ffmpeg -ss ${sss} -t ${dur} -i ${vid}.webm -y -c copy video-${vid}.mp4

# GIF
ffmpeg -ss ${sss} -t ${dur} -i ${vid}.webm -y -vf 'fps=10,scale=320:trunc(ow/a/2)*2:flags=lanczos' gif-${vid}.mkv
ffmpeg -i gif-${vid}.mkv -y -vf palettegen gif-${vid}.png
ffmpeg -i gif-${vid}.mkv -i gif-${vid}.png -filter_complex 'paletteuse' -y gif-${vid}.gif

# Screenshot
ffmpeg -ss ${sss} -t ${dur} -i ${vid}.webm -y -vframes 1 -q:v 2 screenshot-${vid}.jpg

```
