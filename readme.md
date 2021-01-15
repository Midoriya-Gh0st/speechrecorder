# Basic SpeechRecorder clone

`rec.py` contains a basic
[SpeechRecorder](http://www.cstr.ed.ac.uk/research/projects/speechrecorder/) clone written
in Python which should be system-agnostic. Tested using Python 3.7, but 3.6+ should work
well.

This code is set up to record scripts in Festival utts.data format.

This code is not the prettiest, I just wanted a quick tool that works. Currently this tool
spins up a separate process that handles audio recording/playback. I tried using a simple
thread for this, but portaudio would not find the ASIO driver for my audio interface then.
If anyone can figure out how to make this work with threads, that would be better (no while
True: loop needed).

## Prerequisites
Python packages:

* [PySoundFile](https://pysoundfile.readthedocs.io/en/latest/#installation)
* [python-sounddevice](https://python-sounddevice.readthedocs.io/en/latest/installation.html) >= 0.3.15
* [numpy](https://numpy.org/install/)
* [CFFI](https://cffi.readthedocs.io/en/latest/installation.html)

You need to configure the correct Input and Output devices by hand for this tool to work.
Run the following commands to list available audio devices in a Python interpreter:

```python
import sounddevice as sd
print(sd.query_devices())
``` 

The required `in_device` index is marked by `>` and `out_device` by `<`. If the same
device handles both input and output, it will be marked with `*`.
Modify the following lines in `rec.py` with the appropriate device indices, and
set `CHANNEL` to record in mono (default) or stereo (`CHANNEL = [1|2]` respectively):
```python
in_device = 10
out_device = 3
CHANNEL = 1
``` 

The default will record in 44.1 kHz.
If you need higher/lower quality recordings, change `fs` to the required sampling
rate. Default recording setting is 16 bit PCM for WAV files. Check
`soundfile.available_subtypes('WAV')` for alternatives and set `subtype` accordingly in
the `sf.SoundFile` object used in `rec()` if needed.

## How to use
Run `rec.py` with `python rec.py`.

* Press `up` and `down` to navigate sentences
* Press `space` to start/stop recording. Multiple recordings will produce multiple takes
* Press `down` while recording to immediately record the next utterance (without stopping
  in between). 
  * *Warning:* This may lead to bad utterance segmentations (possibly due to timeouts
  used in `multiprocessing.Process.join()`?)
* When not recording, press `p` to listen to the recorded audio (plays the latest take)
* Press `q` to quit.

The tool should parse any script file matching the format of the provided `utts.data`.
For other scripts, provide same-length lists of utterance labels (used for saved file
names) and prompts in the variables `labels` and `utts` respectively.

