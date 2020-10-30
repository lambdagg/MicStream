#!/usr/bin/env python

import pyaudio

pyAudio = pyaudio.PyAudio()
info = pyAudio.get_host_api_info_by_index(0)
count = info.get('deviceCount')

output = False

print("===== INPUT DEVICES =====")

for i in range(0, count):
    if not (pyAudio.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0 and not output:
        print("===== OUTPUT DEVICES =====")
        output = True
    print(i, ["|", " |"][i<10], pyAudio.get_device_info_by_host_api_device_index(0, i).get('name'))