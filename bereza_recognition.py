import vosk
import sys
import sounddevice as sd
import queue


q = queue.Queue()
device = 0
samplerate = int(sd.query_devices(device, 'input')['default_samplerate'])
model = vosk.Model('model_small')

def q_callback(indata, frames, time, status):
    q.put(bytes(indata))

def listen(callback):
    with sd.RawInputStream(samplerate=samplerate, blocksize=16000, device=device,
                            dtype="int16", channels=1, callback=q_callback):
        rec = vosk.KaldiRecognizer(model, samplerate)
        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                callback(rec.Result())
