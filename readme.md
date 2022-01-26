# Basic SpeechRecorder clone

`rec.py` contains a basic [SpeechRecorder](http://www.cstr.ed.ac.uk/research/projects/speechrecorder/) clone written in Python which should be system-agnostic.
This tool can be used to record a set of utterances provided in a script file, and comes with a sample script as used in the [CMU Arctic A](http://festvox.org/cmu_arctic/) speech database.

This repo is intended to support students on the Speech Synthesis course at the University of Edinburgh as they work through [building a unit selection voice](http://speech.zone/exercises/build-a-unit-selection-voice/) from their own recordings.
The original version of this tool was written by [Tim Loderhose](https://github.com/timlod/speechrecorder).

## Setup

If you are using the SLP virtual machine, then you can try and make your audio devices (speaker/microphone) available in the VM, for example through [VirtualBox configuration](https://www.virtualbox.org/manual/UserManual.html#settings-audio).
Otherwise, you may prefer to record data on your local machine and transfer the resulting audio files to another machine to work with Festival.

### Downloading SpeechRecorder

To get the code for SpeechRecorder, you can either download and unzip this repository by clicking the green _Code > Download ZIP_ button above, or clone it directly using `git`:

```git clone https://github.com/dan-wells/speechrecorder```

On Windows, you will probably need to install [Git for Windows](https://gitforwindows.org/) and then run the command above in a _Git Bash_ or _Git CMD_ terminal.

### Installing Python

Python is required to run `rec.py`, along with some non-standard packages.
We have tested most of the recent versions of Python 3, so it shouldn't matter too much which you have available or choose to install.

Click below to expand Python installation instructions for different platforms.

<details>
<summary> Windows </summary>

To install Python on Windows, download an installer from the [Python website](https://www.python.org/downloads/).

The easiest option is to follow the standard installation process.
If you want to customise the install, make sure you tick the checkbox to install ***tcl/tk and IDLE*** – this provides the graphical user interface libraries used by SpeechRecorder.

You may also want to check ***Add Python 3.x to PATH***, so that you can easily launch Python programmes from the command line.

</details>

<details>
<summary> Linux </summary>

Python 3 is probably already installed on your system, and should have the `tkinter` GUI package available.
If not, you may need to install it through your package manager, possibly alongside the PortAudio library for audio handling.

For example, the required packages on Ubuntu might be:

```sudo apt install python3-tk libportaudio2```

</details>

<details>
<summary> Mac </summary>

Mac users may prefer to use the original [SpeechRecorder](http://www.cstr.ed.ac.uk/research/projects/speechrecorder/)!
If not, please follow [these instructions](https://docs.python.org/3/using/mac.html) to install Python 3.

</details>

### Python dependencies

* [PySoundFile](https://pysoundfile.readthedocs.io/en/latest/#installation)
* [python-sounddevice](https://python-sounddevice.readthedocs.io/en/latest/installation.html) >= 0.3.15
* [numpy](https://numpy.org/install/)
* [CFFI](https://cffi.readthedocs.io/en/latest/installation.html)

If you installed `pip` alongside Python, then installing all the necessary dependencies for SpeechRecorder could be as simple as running:

```pip install pysoundfile sounddevice numpy cffi```

It might be preferable not to install these dependencies globally, however.
For additional instructions on creating a Python virtual environment to keep your system tidy, click below.

<details>
<summary> Virtual environments in Python </summary>

Virtual environments are a way of encapsulating Python packages so that projects with different requirements (for example two projects which use different versions of the same package) do not conflict with each other.

After installing Python, you can create a virtual environment using the standard `venv` module:

```python3 -m venv sr-env```

This will create a new directory `sr-env` containing a local copy of the Python interpreter and space to install new packages.
To use this local Python, we must _activate_ the environment:

* **Windows**: `sr-env\Scripts\activate.bat`

* **Linux/Mac**: `source sr-env/bin/activate`

If you see `(sr-env)` somewhere in your command prompt, then it worked!
You can now run the `pip` install command listed above to install the required Python packages in your new virtual environment, leaving the system Python unchanged.

Once you're finished with SpeechRecorder, you can run the `deactivate` command to exit the Python virtual environment.

**Note**: You will need to run the `activate` command whenever you want to use this particular Python environment, after navigating in the terminal to wherever you created the `sr-env` directory.
In general, you might want to keep all your virtual environments in one place, or perhaps create this one inside the directory containing the code for SpeechRecorder.

</details>

## Usage

Run SpeechRecorder like `python rec.py utts.data` (possibly after activating your virtual environment).
You will be presented with a screen showing the first utterance in the file `utts.data`.
Recorded audio will be saved to `recordings/${prompt_label}_${take}.wav`.

The following commands are available:

* `up` and `down` to move between utterances
* `space` to start/stop recording. Multiple recordings will produce multiple takes
* `down` while recording to immediately record the next utterance (without stopping
  in between). 
  * *Warning:* This may lead to bad utterance segmentations (possibly due to timeouts
    used in `multiprocessing.Process.join()`?)
* `p` to listen to the recorded audio (plays the latest take)
* `q` to quit.

### Recording scripts

The tool should parse any script file matching the format of the provided `utts.data`, as described in the [unit selection voice building recipe](http://speech.zone/exercises/build-a-unit-selection-voice/the-recording-script/the-utts-data-file/).
To record your own script, create a new file using the same format and pass it to SpeecRecorder: `python rec.py my_script`

You might want to split the provided `utts.data` into multiple files and use this method to record prompts in multiple sessions.
This will help to overcome the limited interface provided by this version of SpeechRecorder, so that you don't have to scroll through the first 100 prompts to pick up where you left off!

### Audio device configuration

On Windows, once you've set up your Python environment and downloaded SpeechRecorder, everything might Just Work.
On Linux, you may need to do some additional configuration in `rec.py` so that SpeechRecorder knows which audio devices it should use.
For detailed instructions, click below.

<details>
<summary> Audio device configuration </summary>

Run the following commands to list available audio devices in a Python interpreter:

```python
import sounddevice as sd
print(sd.query_devices())
```

The required `in_device` index is marked by `>` and `out_device` by `<`.
If the same device handles both input and output, it will be marked with `*`.

Modify the following lines in `rec.py` with the appropriate device indices:

```python
in_device = 0
out_device = 0
```

By default, recorded audio will be sampled at 44.1 kHz.
If you need higher/lower quality recordings, change the variable `fs` to the required sampling rate.

The default bit depth is 16-bit.
Check `soundfile.available_subtypes('WAV')` for alternatives and set `subtype` accordingly in the `sf.SoundFile` object used in `rec()` if needed.

Audio is recorded in mono by default.
Set `CHANNEL = 2` for stereo recordings.

</details>
