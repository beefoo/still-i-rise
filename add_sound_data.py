# -*- coding: utf-8 -*-

import argparse
import json
import locale
import os
from pprint import pprint
from praat import fileToPitchData
import sys
import time

locale.setlocale(locale.LC_ALL, 'en_US')

# input
parser = argparse.ArgumentParser()
parser.add_argument('-in', dest="INPUT_FILE", default="data/still_i_rise.json", help="Path to input aligned transcript json file")
parser.add_argument('-pf', dest="PITCH_FILE", default="data/still_i_rise.Pitch", help="Path to pitch file")
parser.add_argument('-out', dest="OUTPUT_FILE", default="data/still_i_rise.json", help="Path to output json file")

# init input
args = parser.parse_args()

data = {}
with open(args.INPUT_FILE) as f:
    data = json.load(f)

# Retrieve pitch data from Praat file
frames = fileToPitchData(args.PITCH_FILE)
print "%s frames read from file %s" % (locale.format("%d", len(frames), grouping=True), args.PITCH_FILE)

# Stats
ints = [f["intensity"] for f in frames]
freqs = [f["candidates"][0]["frequency"] for f in frames if len(f["candidates"]) > 0]
print "Freq [%s, %s] Intensities [%s, %s]" % (min(freqs), max(freqs), min(ints), max(ints))

def mean(numbers):
    return float(sum(numbers)) / max(len(numbers), 1)

def getSoundData(start, end, frames):
    frequency = 0
    intensity = 0
    _frames = [f for f in frames if start <= f["start"] < end]

    # calculate mean frequency
    frequencies = [f["candidates"][0]["frequency"] for f in _frames if len(f["candidates"]) > 0]
    if len(frequencies) > 0:
        frequency = mean(frequencies)

    # calculate mean intensity
    intensities = [f["intensity"] for f in _frames]
    if len(intensities) > 0:
        intensity = mean(intensities)

    return {
        "frequency": frequency,
        "intensity": intensity
    }

words = data["words"]
nonwords = data["nonwords"]
lines = data["lines"]

for i, word in enumerate(words):
    soundData = getSoundData(word["start"], word["end"], frames)
    words[i].update(soundData)
    for j, syllable in enumerate(word["syllables"]):
        soundData = getSoundData(syllable["start"], syllable["end"], frames)
        words[i]["syllables"][j].update(soundData)

for i, word in enumerate(nonwords):
    soundData = getSoundData(word["start"], word["end"], frames)
    nonwords[i].update(soundData)

for i, line in enumerate(lines):
    soundData = getSoundData(line["start"], line["end"], frames)
    lines[i].update(soundData)

data["words"] = words
data["nonwords"] = nonwords
data["lines"] = lines

with open(args.OUTPUT_FILE, 'w') as f:
    json.dump(data, f, indent=2)

print "Done."
