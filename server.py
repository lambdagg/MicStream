#!/usr/bin/env python

import pyaudio, socket, select, sys, time

OPTIONS = {
    # Server
    "HOST": "", # Leave blank for any IP.
    "PORT": 4096,
    "MAXCONS": 0, # 0 equals unlimited connections
    "INPUT": 0, # Use devices.py to enter the correct device id here.
    "connCounter": 0, # Socket clients counter

    # Audio
    "CHANNELS": 1,
    "FORMAT": pyaudio.paInt16,
    "BITRATE": 44100,
    "BUFFER": 2048,

    # Core, do not edit!
    "version": "2c1743a391305fbf367df8e4f069f9f9"
}

con = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
con.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

clients = [con]

try:
    con.bind((OPTIONS["HOST"], OPTIONS["PORT"]))
except socket.error:
    print("! Cannot bind host", [OPTIONS["HOST"], "0.0.0.0"][OPTIONS["HOST"] == ""], "with port", OPTIONS["PORT"], "; canceling.")
    sys.exit()

pyAudio = pyaudio.PyAudio()

def data(in_data, frame_count, time_info, status):
    for s in clients[1:]:
        s.send(in_data)
        continue
    return (None, pyaudio.paContinue)

audioStream = pyAudio.open(format=OPTIONS["FORMAT"], channels=OPTIONS["CHANNELS"], rate=OPTIONS["BITRATE"], input=True, input_device_index=OPTIONS["INPUT"], frames_per_buffer=OPTIONS["BUFFER"], stream_callback=data)

con.listen(OPTIONS["MAXCONS"])
print("* Socket is now listening on port", OPTIONS["PORT"], "with", [OPTIONS["MAXCONS"], "0(unlimited)"][OPTIONS["MAXCONS"] == 0], "number of maximum connections.")

try:
    while 1:
        r, w, e = select.select(clients, [], [])
        for s in r:
            if s is con:
                client, address = con.accept()
                clients.append(client)
                print("* New client connected as %s:%s" % (address[0], address[1]))
            else:
                try:
                    data = s.recv(1024)
                    if not data:
                        clients.remove(s)
                        print("* Client %s disconnected." % (s))
                except ConnectionResetError:
                    clients.remove(s)
except KeyboardInterrupt:
    pass

con.close()
print("* Socket closed.")

audioStream.stop_stream()
print("* Audio stream stopped, recording done.")

audioStream.close()
print("* Audio stream closed.")

pyAudio.terminate()
print("* PyAudio terminated.")