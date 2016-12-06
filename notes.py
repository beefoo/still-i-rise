# -*- coding: utf-8 -*-

import argparse
import json
import math
import os
from pprint import pprint
import sys
import time

# input
parser = argparse.ArgumentParser()
parser.add_argument('-in', dest="INPUT_FILE", default="data/still_i_rise.json", help="Path to input aligned transcript json file")

# init input
args = parser.parse_args()

# pitch
def freqToNote(freq):
    if freq <= 0:
        return ("NONE", 0)
    notes = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    A4 = 440
    C0 = A4 * math.pow(2, -4.75)
    h = int(round(12*(math.log(freq/C0)/math.log(2))))
    octave = h / 12 - 1
    octave = max(octave, 0)
    n = h % 12
    return (notes[n], octave)

data = {}
with open(args.INPUT_FILE) as f:
    data = json.load(f)

words = data["words"]
syllableNotes = {}

for word in words:
    for syll in word["syllables"]:
        (note, octave) = freqToNote(syll["frequency"])
        key = note + str(octave)
        if key in syllableNotes:
            syllableNotes[key] += 1
        else:
            syllableNotes[key] = 1

syllableNotes = [{"note": k, "count": v} for k, v in syllableNotes.iteritems()]
syllableNotes = sorted(syllableNotes, key=lambda n: -n["count"])

pprint(syllableNotes)
