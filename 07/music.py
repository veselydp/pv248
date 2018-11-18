import wave
import struct
import numpy as np
import sys
from math import log2, pow

max = 0
min = 0
A4 = int(sys.argv[1])
C0 = A4*pow(2, -4.75)
name = ["c", "cis", "d", "es", "e", "f", "fis", "g", "gis", "a", "bes", "b"]
peaksArr = []

def pitch(freq):
    h = 12*log2(freq/C0)
    deviation = h
    h = round(h)
    deviation = round((deviation - h) * 100)
    n = h % 12
    totalName = name[n]
    if h // 12 < 2:
        totalName = totalName[0].upper()
        for item in range(0,h // 12):
            totalName = totalName + ","
    if h // 12 == 2:
        totalName = totalName[0].upper() + totalName[1:]
    if h // 12 > 2:
        for item in range(0,h // 12 - 3):
            totalName = totalName + "'"
    if deviation > 0: totalName = totalName + ("+") + str(deviation)
    else:
        totalName = totalName + str(deviation)
    return totalName


def structUnpackFun(frames, nOfFrames):
    nOfFrames = int(nOfFrames)
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
    data=tempVarArr
    return data

def returnAvg(data, framerate):
    threshold = 20
    amplNp = np.fft.rfft(data)
    amplNp = np.abs(amplNp)

    avgAmpl = np.average(amplNp)
    return (avgAmpl*20, amplNp)


sound_file = wave.open(sys.argv[2], "r")
framerate = sound_file.getframerate()
nOfFrames = sound_file.getnframes()
nOfChannels = sound_file.getnchannels()
repeated = int(nOfFrames/framerate)*10
duration = nOfFrames/framerate
frames = sound_file.readframes(int(framerate))
data = structUnpackFun(frames, nOfChannels * framerate)



if (nOfChannels == 2):
    data = convertStereo(data)
else: data = list(data)

winPos = 0.1
globalPeaks = []

for i in range(0,repeated):
    currWindPeaks = []
    amplAvg, amplArr = returnAvg(data, framerate)


    for index, amplitude in enumerate(amplArr):
        if amplitude >= amplAvg:
            currWindPeaks.append([])
            currWindPeaks[-1].append(index)
            currWindPeaks[-1].append(amplitude)



    currWindPeaks= sorted(currWindPeaks, key=lambda x: x[1], reverse=True)
    currWindPeaks = currWindPeaks[:3]
    currWindPeaks = sorted(currWindPeaks, key=lambda x: x[0], reverse=False)
    pitchStr = ""
    for index, peak in enumerate(currWindPeaks):
        pitchStr += " "
        pitchStr += pitch(peak[0])
    if len(peaksArr) != 0 and pitchStr ==  peaksArr[-1][0]:
            peaksArr[-1][1] = winPos
    else:
            peaksArr.append([])
            peaksArr[-1].append(pitchStr)
            peaksArr[-1].append(winPos)
            peaksArr[-1].append(winPos-0.1)

    winPos = winPos + 0.1

    del data[:(int(framerate * 0.1))]
    #data = data[(int(framerate * 0.1)):]

    if winPos -0.1 + 1 < duration:
        frames = sound_file.readframes(int(framerate * 0.1))
        if (nOfChannels == 2):
            dat2 = convertStereo(structUnpackFun(frames, nOfChannels * framerate * 0.1))

        else:
            dat2 = structUnpackFun(frames, nOfChannels * framerate * 0.1)
        data += dat2
    if (duration - winPos < 0.9): break

for peak in peaksArr:
    peak[2] = str(round(peak[2],2)).zfill(2)
    print( peak[2] + "-"  + str(round(peak[1],2)).zfill(2) + peak[0])






#absArr =np.array_split(absArr, repeated*10)



