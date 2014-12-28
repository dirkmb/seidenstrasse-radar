import pyaudio
import wave
import time
import sys
import numpy as np
import struct


# instantiate PyAudio (1)
p = pyaudio.PyAudio()
SRATE = 44100
# define callback (2)
offset=0
rec = []

# set limits
MIN_MAX_LEVEL=500

def callback_in(in_data, frame_count, time_info, status):
    global rec
    #rec=np.append(rec, np.fromstring(in_data, dtype=np.int16))
    fdata = np.fromstring(in_data, dtype=np.int16)
    rec.append(fdata)

    print("in",fdata)
    return (in_data, pyaudio.paContinue)

def callback_out(in_data, frame_count, time_info, status):
    global offset
    fdata = np.int16(np.sin(((np.arange(frame_count)+offset)/SRATE)*2*np.pi*1e3)*30e3)
    data = fdata.tobytes()
    offset+=frame_count
    print("out",fdata)
    if offset > 100*1024:
        print("fin")
        return (None, pyaudio.paComplete)
    elif offset >= 10*1024 and offset <= 10*1024:
        print("sin")
        return (data, pyaudio.paContinue)
    else:
        print("null")
        return (np.arange(frame_count).tobytes(), pyaudio.paContinue)
    print(fdata)
    return (data, pyaudio.paContinue)

# open stream using callback (3)
stream_in = p.open(format=pyaudio.paInt16,
                channels=1,
                rate=SRATE,
                #output=True,
                input=True,
                stream_callback=callback_in)

# open stream using callback (3)
stream_out = p.open(format=pyaudio.paInt16,
                channels=1,
                rate=SRATE,
                output=True,
                #input=True,
                stream_callback=callback_out)

# start the stream (4)
stream_in.start_stream()
stream_out.start_stream()


# wait for stream to finish (5)
while stream_out.is_active():
    time.sleep(0.1)

# stop stream (6)
stream_out.stop_stream()
stream_out.close()

stream_in.stop_stream()



import matplotlib.pyplot as plt
plt.plot(rec)
plt.show()

for r in rec:
#    print(r,np.max(r),np.min(r))
    r *= (np.max(r) > MIN_MAX_LEVEL)
    r *= (np.min(r) < -MIN_MAX_LEVEL)
plt.plot(rec)
plt.show()

# close PyAudio (7)
p.terminate()
