# -*- coding: utf-8 -*-

# Based on: https://github.com/aubio/aubio/blob/master/python/demos/demo_pitch.py

import argparse
import aubio
import json
import locale
import math
import os
from pprint import pprint
import sys
import time

locale.setlocale(locale.LC_ALL, 'en_US')

# input
parser = argparse.ArgumentParser()
parser.add_argument('-in', dest="INPUT_FILE", default="data/still_i_rise.json", help="Path to input aligned transcript json file")
parser.add_argument('-out', dest="OUTPUT_FILE", default="data/still_i_rise.json", help="Path to output json file")
parser.add_argument('-cd', dest="CLIPS_DIR", default="clips/", help="Path to clips dir")
parser.add_argument('-ce', dest="CLIP_EXT", default=".wav", help="Clip extension")
parser.add_argument('-sr', dest="SAMPLERATE", type=int, default=44100, help="Sample rate")
parser.add_argument('-fft', dest="FFT_SIZE", type=int, default=4096, help="FFT size")
parser.add_argument('-hop', dest="HOP_SIZE", type=int, default=512, help="Hop size")
parser.add_argument('-tol', dest="TOLERANCE", type=float, default=0.8, help="Tolerance")

# init input
args = parser.parse_args()
CLIPS_DIR = args.CLIPS_DIR
CLIP_EXT = args.CLIP_EXT
SAMPLERATE = args.SAMPLERATE
FFT_SIZE = args.FFT_SIZE
HOP_SIZE = args.HOP_SIZE
TOLERANCE = args.TOLERANCE

data = {}
with open(args.INPUT_FILE) as f:
    data = json.load(f)
words = data["words"]
nonwords = data["nonwords"]
lines = data["lines"]

def mean(arr):
    if len(arr) <= 0:
        return 0
    return float(sum(arr)) / max(len(arr), 1)

def weightedAvg(arr, weights):
    if len(arr) <= 0:
        return 0
    return sum(arr[g] * weights[g] for g in range(len(arr))) / sum(weights)

def rootMeanSquare(arr):
    rms = 0
    for val in arr:
        rms += (val * val);
    return math.sqrt(rms/len(arr));

def getSoundData(filename, samplerate, fftsize, hopsize, tolerance):
    s = aubio.source(filename, samplerate, hopsize)
    samplerate = s.samplerate

    pitch_o = aubio.pitch("yin", fftsize, hopsize, samplerate)
    pitch_o.set_unit("Hz") # or midi, bin, cent
    pitch_o.set_tolerance(tolerance)

    frequencies = []
    intensities = []
    weights = []
    frequency = 0
    intensity = 0

    # total number of frames read
    total_frames = 0
    while True:
        samples, read = s()
        pitch = pitch_o(samples)[0]
        rms = rootMeanSquare(samples)
        # pitch = int(round(pitch))
        confidence = pitch_o.get_confidence()
        #if confidence < 0.8: pitch = 0.
        # print("%f %f %f" % (total_frames / float(samplerate), pitch, confidence))
        if pitch > 0:
            frequencies.append(pitch)
            weights.append(confidence)
        if rms > 0:
            intensities.append(rms)
        total_frames += read
        if read < hopsize: break

    return {
        "frequency": round(weightedAvg(frequencies, weights), 2),
        "intensity": round(mean(intensities), 2)
    }

print "Analyzing words..."
for i, word in enumerate(words):
    filename = CLIPS_DIR + "words/" + word["name"] + CLIP_EXT
    soundData = getSoundData(filename, SAMPLERATE, FFT_SIZE, HOP_SIZE, TOLERANCE)
    words[i].update(soundData)
    for j, syllable in enumerate(word["syllables"]):
        filename = CLIPS_DIR + "syllables/" + syllable["name"] + CLIP_EXT
        soundData = getSoundData(filename, SAMPLERATE, FFT_SIZE, HOP_SIZE, TOLERANCE)
        words[i]["syllables"][j].update(soundData)

print "Analyzing nonwords..."
for i, word in enumerate(nonwords):
    filename = CLIPS_DIR + "nonwords/" + word["name"] + CLIP_EXT
    soundData = getSoundData(filename, SAMPLERATE, FFT_SIZE, HOP_SIZE, TOLERANCE)
    nonwords[i].update(soundData)

print "Analyzing lines..."
for i, line in enumerate(lines):
    filename = CLIPS_DIR + "lines/" + line["name"] + CLIP_EXT
    soundData = getSoundData(filename, SAMPLERATE, FFT_SIZE, HOP_SIZE, TOLERANCE)
    lines[i].update(soundData)

data["words"] = words
data["nonwords"] = nonwords
data["lines"] = lines

with open(args.OUTPUT_FILE, 'w') as f:
    json.dump(data, f, indent=2)

print "Done."
