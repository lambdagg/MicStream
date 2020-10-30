#!/usr/bin/env python

import pyaudio, socket, sys, time

OPTIONS = {
    # Client
    "HOST": "localhost",
    "PORT": 8120,
    "OUTPUT": 0, # Use devices.py to enter the correct device id here.
    "connCounter": 0, # Socket clients counter

    # Audio
    "CHANNELS": 1,
    "FORMAT": pyaudio.paInt16,
    "BITRATE": 44100,
    "BUFFER": 4096,

    # Core, do not edit!
    "version": "2c1743a391305fbf367df8e4f069f9f9"
}

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
client.connect((OPTIONS["HOST"], OPTIONS["PORT"]))
audio = pyaudio.PyAudio()
stream = audio.open(format=OPTIONS["FORMAT"], channels=OPTIONS["CHANNELS"], rate=OPTIONS["BITRATE"], output=True, output_device_index=OPTIONS["OUTPUT"], frames_per_buffer=OPTIONS["BUFFER"])

try:
    print("* Connected to %s:%s" % (OPTIONS["HOST"], OPTIONS["PORT"]))
    while 1:
        data = client.recv(OPTIONS["BUFFER"])
        stream.write(data)
except KeyboardInterrupt:
    pass

print("* Going offline")
client.close()
print("* Connection closed")
stream.close()
print("* Audio stream closed")
audio.terminate()
print("* Audio stream terminated")