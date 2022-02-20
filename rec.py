import queue
import sys
import tkinter as tk
from collections import defaultdict
from multiprocessing import Process, Value
from pathlib import Path
from time import sleep

import sounddevice as sd
import soundfile as sf
# import cffi
# import

# 使用指令: python rec.py utts.data

if len(sys.argv) != 2:
    sys.exit("Usage: python rec.py utts.data")
else:
    _, utts = sys.argv

path = Path("recordings")
path.mkdir(exist_ok=True)

with open(utts) as f:
    script = [i.strip('( )"\n').split(' "') for i in f.readlines()]
labels, utts = zip(*script)
takes = defaultdict(int)
for i in labels:
    while (path / "{}_{}.wav".format(i, takes[i] + 1)).is_file():
        takes[i] += 1

print(sd.query_devices())
in_device = 0
out_device = 0
sd.default.device = [in_device, out_device]

CHANNEL = 1
fs = 16000  # hz, = 44.1 kHz, need to be changed to 16kHz, = 16000
sd.default.samplerate = fs


def audio_process(labels, play, record, i):
    while True:
        if record.value:
            rec(labels[i.value], record)
        if play.value:
            playback(labels[i.value])
            play.value = 0
        sleep(0.1)


def playback(name):
    wav_file = path / "{}_{}.wav".format(name, takes[name])
    print("Playback", wav_file)
    if wav_file.is_file():
        data, fs = sf.read(str(wav_file))
    else:
        data, fs = sf.read(str(path / "not_found.wav"))
    sd.play(data, fs)


def rec(name, record):
    q = queue.Queue()

    def callback(indata, frames, time, status):
        """This is called (from a separate thread) for each audio block."""
        if status:
            print(status, file=sys.stderr)
        q.put(indata.copy())

    takes[name] += 1
    wav_file = str(path / "{}_{}.wav".format(name, takes[name]))
    print("Recording", wav_file)
    # Make sure the file is opened before recording anything:
    with sf.SoundFile(wav_file, mode='w', samplerate=fs, channels=CHANNEL,
                      subtype='PCM_16') as file:
        with sd.InputStream(samplerate=fs, device=in_device, channels=CHANNEL,
                            callback=callback):
            while record.value:
                file.write(q.get())


# Recorder GUI
if __name__ == "__main__":
    i = 0
    i_mp = Value('i', i)
    record = Value('i', 0)
    play = Value('i', 0)

    root = tk.Tk()
    text = tk.StringVar()
    label = tk.StringVar()
    text.set("{}".format(utts[i]))
    label.set("{}:".format(labels[i]))

    p = Process(target=audio_process, args=(labels, play, record, i_mp))
    p.daemon = True
    p.start()

    def key(event):
        global i, play
        code = event.keysym
        i_mp.value = i

        if code == 'space':
            # Record/stop recording - space
            if record.value == 0:
                record.value = 1
            else:
                record.value = 0
            l.config(fg="green" if not record.value else "red")
            p.join(0)
        elif code == 'p':
            # Play/pause - p
            play.value = 1
            p.join(0)
            set_colour = lambda c: l.config(fg=c)
            set_colour("yellow")
            frame.after(1000, lambda: set_colour("green"))
        elif code == 'Up':
            # up
            if i <= 0:
                i = -1
                text.set("This was the first sentence! Go forward instead!")
            else:
                i -= 1
                text.set("{}".format(utts[i]))
                label.set("{}".format(labels[i]))

        elif code == 'Down':
            # down
            if i == len(utts) - 1:
                i = len(utts)
                text.set("End of list already reached! Go back :)")
                if record.value:
                    record.value = 0
                    p.join(0)
                    l.config(fg="green")
            else:
                i += 1
                text.set("{}".format(utts[i]))
                label.set("{}".format(labels[i]))
                if record.value:
                    i_mp.value = i
                    record.value = 0
                    p.join(0.01)
                    record.value = 1
                    p.join(0)
        elif code == 'q':
            # quit - q
            p.terminate()
            root.destroy()

    frame = tk.Frame(root, width=900, height=900)
    frame.bind("<Key>", key)
    frame.pack()
    frame.focus_set()

    ll = tk.Label(textvariable=label, fg="green", font=("Helvetica", 60),
                  anchor="sw", justify="left")
    # Make wraplength some function of window size and adjust placement
    # accordingly in the future
    l = tk.Label(textvariable=text, fg="green", font=("Helvetica", 60),
                 anchor="center", justify="center", wraplength=700)
    ll.place(y=0)
    l.place(rely=0.1, relx=0.2)

    root.mainloop()
