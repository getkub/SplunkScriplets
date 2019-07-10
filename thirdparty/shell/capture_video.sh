#!/bin/sh

# https://www.youtube.com/watch?v=BBvod49uySQ
printf "Input URL: "
read URL
youtube-dl -f 'bestaudio[ext=m4a]'  $URL

#Capture Videos
