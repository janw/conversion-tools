#!/usr/bin/env python3

import subprocess
import fnmatch
import os
import json

base_path   = '/Volumes/Musik/'
out_path    = '/Volumes/SD Card/iTunes Music/'
ft_input    = '.flac'
ft_output   = '.m4a'
postscript  = """
                on run {argv}
                    repeat with i from 1 to number of items in argv
                        tell application "iTunes"
                            launch
                            add (item i of argv as POSIX file)
                        end tell
                    end repeat
                end run
              """

conv_bin = '/usr/local/bin/ffmpeg -loglevel error'.split(' ')
impl_bin = 'atomicparsley'
conv_options = '-y -c:a libfaac -q:a 500 cover.jpg'.split(' ')
conv_options_retry = '-y -vn -c:a libfaac -q:a 500'.split(' ')
impl_options = '--artwork cover.jpg --overWrite'.split(' ')
conv_output = ''

def main():
    files = []
    addable_list = []
    succeeded   = 0
    failed      = 0
    global conv_output

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

            print(conv_input)

            # Compile all command line options
            args_conv = conv_bin + conv_input + conv_options + [conv_output]
            args_impl = [impl_bin, conv_output] + impl_options

            # Run conversion and implantation of the cover art
            conv = subprocess.call(args_conv, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

            # Check of one of the two failed
            if conv != 0:
                args_conv2 = conv_bin + conv_input + conv_options_retry + [conv_output]
                conv = subprocess.call(args_conv2, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

            else:
                impl = subprocess.call(args_impl, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

                if impl != 0:
                    print('Failed implanting cover art. No artwork in input?')
                    print(args_impl)

                try:
                    os.remove('cover.jpg')
                except FileNotFoundError:
                    pass

            if conv == 0:
                succeeded +=1
                addable_list.append(conv_output)
            else:
                failed +=1
                print('Failed conversion with parameters:')
                print(' '.join([arg.replace(' ', '\ ') for arg in args_conv]))

                try:
                    os.remove(conv_output)
                except FileNotFoundError:
                    pass

            if succeeded > 2:
                    break
        if succeeded > 2:
            break

    print('Converted {} files, {} failed.'.format(succeeded, failed))

    if len(addable_list) > 0 and len(postscript) > 0:

        import applescript
        scpt = applescript.AppleScript(postscript)
        print(scpt.run(addable_list))

if __name__ == "__main__":

    try:
        main()
    except KeyboardInterrupt:

        # Delete the current (incomplete) file
        try:
            os.remove(conv_output)
        except FileNotFoundError:
            pass
        print("\nQuit early.")