# Collection of conversion tools and scripts

I regularly find myself in situations where certain conversion tasks take up a lot of time when done manually. This repository is supposed to alleviate that. Whenever I stumble upon a task that can be done in batch or by handling through a script, I'll add it to this collection.

In my personal quest to learn more about Python and establish it as my personal programming language of choice, I am going to implement using Python 3 (if not noted otherwise). This might be senseless (for example, when a simple bash script would suffice and handle things faster and easier), but I see it as a personal challenge.

## convert-flac2aac.py

This script handles converting my collection of ripped CDs (in FLAC format) to AAC (contained in m4a files) as used in the context of iTunes. Unfortunately my preference for FLAC for lossless coding does not go well with the wish to have the content available in iTunes (especially home sharing) aswell.

The script converts all FLAC files given in `base_path` and saves them to `out_path` as M4A files. It uses ffmpeg (built with libfaac) to do the conversion and AtomicParsley to handle the insertion of album artwork metadata. Files are converted at an extremly high lossy quality setting of the libfaac encoder.

After conversion, all files of the batch are imported into iTunes using a simple AppleScript script. Considering this step, the entire conversion process could easily be done in AppleScript. But what the heck.

**Pros:**

* Does what it should. Files are converted, new files only require a re-execution of the script and are added properly
* Conversion options are relatively easy to adjust (if needed)

**Cons:**

* Execution of AppleScript from within Python requires `applescript`, and `pyobjc` packages to be installed, which require separate compilation. This is an extreme hassle for this purpose.
* Conversion could be streamlined in a shell script or an AppleScript script.

### Requirements

* Mac OS X (as it uses Apple Script)
* Python 3
* Python packages `applescript`, and `pyobjc`


## License

The contents of this repository are published under CC0, otherwise known as Public Domain.

> The person who associated a work with this deed has dedicated the work to the public domain by waiving all of his or her rights to the work worldwide under copyright law, including all related and neighboring rights, to the extent allowed by law.

> You can copy, modify, distribute and perform the work, even for commercial purposes, all without asking permission. See Other Information below.
