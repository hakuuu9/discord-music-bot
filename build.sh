#!/bin/bash

# Download static ffmpeg binary
mkdir -p ffmpeg
cd ffmpeg
curl -L https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz -o ffmpeg.tar.xz
tar -xf ffmpeg.tar.xz --strip-components=1
chmod +x ffmpeg

# Move back to project root
cd ..
