#!/usr/bin/env python3

import subprocess
import fnmatch
import os
import json

base_path   = '/Volumes/Musik/'
out_path    = '/Volumes/Data HD/iTunes Media/Automatically Add to iTunes.localized/'
ft_input    = '.flac'
ft_output   = '.m4a'

conv_bin = '/usr/local/bin/ffmpeg -loglevel error'.split(' ')
conv_options = '-c:a libfaac -q:a 500'.split(' ')
files = []
succeeded   = 0
failed      = 0

for root, dirnames, filenames in os.walk(base_path):
    for filename in fnmatch.filter(filenames, '*' +ft_input):
        cur_outfile = os.path.splitext(filename)[0]+ft_output
        conv_input = ['-i', os.path.join(root, filename)]

        # If no outpath is defined, use the input directories
        if out_path is None:
            conv_output = os.path.join(root, os.path.splitext(filename)[0])

        # With out_recurse, we'll recursively create subdirectories in out_path
        else:
            cur_dir = os.path.join(out_path, root[len(base_path):])
            conv_output = os.path.join(cur_dir, cur_outfile)

            os.makedirs(cur_dir, exist_ok=True)

        if os.path.isfile(conv_output):
            continue

        args = conv_bin + conv_input + conv_options + [conv_output]
        conv = subprocess.Popen(args, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)

        if not conv.returncode:
            failed +=1
            print(conv.args)
            print(conv.stderr.read())
        else:
            succeeded +=1

print('Converted {} files, {} failed.'.format(succeeded, failed))

