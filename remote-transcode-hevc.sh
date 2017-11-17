#!/usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'

ssh_credentials="user@workstation"

ssh_dir="/mnt/tank/video"
ssh_glob="${ssh_dir}/*p.mkv"

output_dir="/Volumes/Untitled"

renderer=/dev/dri/renderD129

ffmpeg_bin=/home/ja1034/bin/ffmpeg
ffmpeg_opts=" \
    -y \
    -hwaccel vaapi \
    -hwaccel_device ${renderer} \
    -hwaccel_output_format vaapi \
    -i \\\"\$file\\\" \
    -c:a copy \
    -c:v hevc_vaapi \
    -profile:v 1 \
    -crf 28 \
    -f matroska \
    pipe:1"

input_files=`ssh $ssh_credentials "ls ${ssh_glob}"`

for file in $input_files; do
    filename=$(basename "${file}")
    echo "next file: $filename"

    cmd=$(eval echo "$ffmpeg_bin $ffmpeg_opts")
    ssh $ssh_credentials "$cmd" | \
        cat > "${output_dir}/${filename}.x265.mkv"
done
