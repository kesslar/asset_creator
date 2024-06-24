#!/bin/bash

#Define some variables
jpg_assets_dir="$HOME/Pictures/Assets"
video_assets_dir="$HOME/Pictures/Assets/Video_assets"

#Find the basename for all of the files in this directory
for file in "$jpg_assets_dir"/*.jpg; do
  base_name=$(basename "$file" .jpg)

  #Check if the location of the video_assets_dir variable exsist and creates it if it doesn't
  if [ ! -d "$video_assets_dir" ]; then
    mkdir -p "$video_assets_dir"
  fi

  #Convert the files from jpg to mp4 and place the mp4 files into the video_assets_dir location
  ffmpeg -loop 1 -i "$file" -c:v libx265 -r 1 -t 300 -pix_fmt yuv420p -vf scale=1920:1080 -threads 16 "$video_assets_dir/$base_name.mp4"
done
