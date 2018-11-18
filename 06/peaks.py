import wave
import struct
import numpy as np
import sys

max = 0
min = 0

def structUnpackFun(frames, nOfFrames):
    data = struct.unpack(str(nOfFrames) + "h", frames)
    return data

def convertStereo(data):
    tempVarArr = []
    for i in range(0,len(data)):
            if i % 2 ==0:
                tempVar = data[i]
            else:
                tempVar = (tempVar + data[i]) / 2
                tempVarArr.append(tempVar)
    data=np.array(tempVarArr)
    return data

def returnAvg(data, framerate):
    threshold = 20
    average = np.fft.rfft(data) / framerate
    average = np.abs(average)
    absArr = average
    average = np.average(average)
    return (average * threshold, absArr)


sound_file = wave.open(sys.argv[1], "r")
framerate = sound_file.getframerate()
nOfFrames = sound_file.getnframes()
nOfChannels = sound_file.getnchannels()
repeated = int(nOfFrames/framerate)
for i in range(0,repeated):
        frames = sound_file.readframes(framerate)
        data = structUnpackFun(frames, nOfChannels * framerate)
        data = np.array(data)

        if (nOfChannels == 2): data = convertStereo(data)

        average, absArr = returnAvg(data, framerate)

        i = 0
        for item in absArr:
            if item > average:
                if max < i: max = i
                if min == 0: min = i
            i = i + 1

        #w = np.fft.fft(data)
        #freqs = np.fft.fftfreq(len(w))

        #dx = np.argmax(np.abs(w))

        #freq = freqs[idx]
        #freq_in_hertz = abs(freq * framerate)
        #print(freq_in_hertz)
if max != 0: print("low = " + str(min) + ", high = " + str(max))
else: print("no peaks")
