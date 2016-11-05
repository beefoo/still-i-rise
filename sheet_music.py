# -*- coding: utf-8 -*-

import argparse
import json
import os
from pprint import pprint
from lilypond import lily
import sys
import time

# input
parser = argparse.ArgumentParser()
parser.add_argument('-in', dest="INPUT_FILE", default="data/still_i_rise.json", help="Path to input aligned transcript json file")
parser.add_argument('-out', dest="OUTPUT_FILE", default="data/still_i_rise.py", help="Path to output lilypond file")
parser.add_argument('-tempo', dest="TEMPO", type=int, default=120, help="Tempo in BPM")

# init input
args = parser.parse_args()
TEMPO = args.TEMPO

# note durations in ms
quarterMs = 60000 / TEMPO
measureMs = quarter * 4

data = {}
with open(args.INPUT_FILE) as f:
    data = json.load(f)

header = {
    "title": "Still I Rise",
    "subtitle": "Maya Angelou",
    "composer": "As performed by Maya Angelou",
    "arranger": "Arranged by Brian Foo",
    "copyright": "Learn more at brianfoo.com"
}
music = {
    "tempo": TEMPO,
    "relative": "c",
    "measures": []
}
measures = []
lyrics = []

currentMeasure = {
    "notes": [],
    "duration": 0
}
for i, word in enumerate(data):
    for j, syllable in enumerate(word["syllables"]):

music["measures"] = measures
lilyString = lily(music, lyrics, header)

with open(args.OUTPUT_FILE, "w") as f:
    f.write(lilyString)
    print "Wrote %s measures to file %s" % (len(music), args.OUTPUT_FILE)
