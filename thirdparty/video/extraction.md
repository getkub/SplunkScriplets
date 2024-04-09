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
ffmpeg -ss ${sss} -t ${dur} -i ${vid}.webm -y -vn -acodec copy audio-${vid}.mp3


```
