# -*- coding: utf-8 -*-

import argparse
import json
import math
import os
from pprint import pprint
import lib.lilypond as lilypond
import sys
import time

# input
parser = argparse.ArgumentParser()
parser.add_argument('-in', dest="INPUT_FILE", default="data/still_i_rise.json", help="Path to input aligned transcript json file")
parser.add_argument('-out', dest="OUTPUT_FILE", default="data/still_i_rise.ly", help="Path to output lilypond file")
parser.add_argument('-tempo', dest="TEMPO", type=int, default=240, help="Tempo in BPM")
parser.add_argument('-sn', dest="SHORTEST_NOTE", type=int, default=16, help="Smallest note, e.g. 16 = 1/16th note")
parser.add_argument('-octave', dest="ADJUST_OCTAVE", type=int, default=-1, help="Amount to adjust octave, e.g. -1 will lower all notes by one octave")

# init input
args = parser.parse_args()
TEMPO = args.TEMPO
SHORTEST_NOTE = args.SHORTEST_NOTE
ADJUST_OCTAVE = args.ADJUST_OCTAVE

# note durations in ms
quarterMs = 60000 / TEMPO
measureMs = quarterMs * 4
minNoteMs = measureMs / SHORTEST_NOTE

print "Quarter note: %s, Measure: %s, Min note: %s" % (quarterMs, measureMs, minNoteMs)

data = {}
with open(args.INPUT_FILE) as f:
    data = json.load(f)

header = {
    "title": "Still I Rise",
    "subtitle": "Maya Angelou",
    "composer": "As performed by Maya Angelou",
    "arranger": "Arranged by Brian Foo"
    # "copyright": "Learn more at brianfoo.com"
}
layout = {
    "layout-set-staff-size": 14
}
music = {
    "tempo": TEMPO,
    "notes": []
}
lyrics = []

# Add syllables
notes = []
for i, word in enumerate(data["words"]):
    for j, syllable in enumerate(word["syllables"]):
        notes.append({
            "note": lilypond.freqToNote(syllable["frequency"], ADJUST_OCTAVE),
            "start": int(round(syllable["start"] * 1000)),
            "end": int(round(syllable["end"] * 1000)),
            "text": syllable["text"]
        })
        if j > 0:
            lyrics.append({
                "start": int(round(syllable["start"] * 1000)),
                "text": "--"
            })
        lyrics.append({
            "start": int(round(syllable["start"] * 1000)),
            "text": syllable["text"]
        })

# Add non-words
for i, word in enumerate(data["nonwords"]):
    notes.append({
        "note": lilypond.freqToNote(word["frequency"], ADJUST_OCTAVE),
        "start": int(round(word["start"] * 1000)),
        "end": int(round(word["end"] * 1000)),
        "text": "x"
    })
    lyrics.append({
        "start": int(round(word["start"] * 1000)),
        "text": "x"
    })
lyrics = sorted(lyrics, key=lambda l: l["start"])

# Normalize and print to lilypond syntax
music["notes"] = lilypond.normalizeNotes(notes, TEMPO, SHORTEST_NOTE)
lilyString = lilypond.toString(music, lyrics, header, layout)

# pprint([(n["text"], n["note"]) for n in music["notes"][30:50]])
# sys.exit(1)

with open(args.OUTPUT_FILE, "w") as f:
    f.write(lilyString)
    print "Wrote %s notes to file %s" % (len(notes), args.OUTPUT_FILE)
