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
parser.add_argument('-af', dest="ANALYSIS_FILE", default="data/still_i_rise_sound.json", help="Path to input sound analysis json file")
parser.add_argument('-out', dest="OUTPUT_FILE", default="data/still_i_rise.ly", help="Path to output lilypond file")
parser.add_argument('-tempo', dest="TEMPO", type=int, default=240, help="Tempo in BPM")
parser.add_argument('-sn', dest="SHORTEST_NOTE", type=int, default=8, help="Smallest note, e.g. 16 = 1/16th note")
parser.add_argument('-mo', dest="MAX_OCTAVE", type=int, default=7, help="Max octave")
parser.add_argument('-octave', dest="ADJUST_OCTAVE", type=int, default=-1, help="Amount to adjust octave, e.g. -1 will lower all notes by one octave")

# init input
args = parser.parse_args()
TEMPO = args.TEMPO
SHORTEST_NOTE = args.SHORTEST_NOTE
ADJUST_OCTAVE = args.ADJUST_OCTAVE
MAX_OCTAVE = args.MAX_OCTAVE

# note durations in ms
quarterMs = 60000 / TEMPO
measureMs = quarterMs * 4
minNoteMs = measureMs / SHORTEST_NOTE
minSlurMs = minNoteMs * 3

print "Quarter note: %s, Measure: %s, Min note: %s" % (quarterMs, measureMs, minNoteMs)

data = {}
with open(args.INPUT_FILE) as f:
    data = json.load(f)
transcript = data["transcript"]

analysis = {}
with open(args.ANALYSIS_FILE) as f:
    analysis = json.load(f)

header = {
    "title": "Still I Rise",
    "subtitle": "Maya Angelou",
    "composer": "As performed by Maya Angelou",
    "arranger": "Arranged by Brian Foo"
    # "copyright": "Learn more at brianfoo.com"
}
# thresholds for dynamic marks
dynamics = [
    {"mark": "f", "intensity": 0.999},
    {"mark": "", "intensity": 0.3 },
    {"mark": "p", "intensity": 0.2},
    {"mark": "pp", "intensity": 0}
]
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
    firstLetter = transcript[word["startOffset"]]
    charAfter = transcript[min(word["endOffset"], len(transcript)-1)].strip()
    for j, syllable in enumerate(word["syllables"]):
        # check for capitalization
        if j <= 0:
            syllable["text"] = firstLetter + syllable["text"][1:]
        # check for punctation
        if j >= (len(word["syllables"])-1) and not charAfter.isalpha():
            syllable["text"] += charAfter
        # add note
        if syllable["name"] in analysis and "primaryFrames" in analysis[syllable["name"]]:
            frames = analysis[syllable["name"]]["primaryFrames"]
            intensity = analysis[syllable["name"]]["maxIntensity"]
            start = int(round(syllable["start"] * 1000))
            end = int(round(syllable["end"] * 1000))
            notes.append({
                "notes": lilypond.framesToNotes(frames, start, end, minSlurMs, ADJUST_OCTAVE, MAX_OCTAVE),
                "start": start,
                "end": end,
                "intensity": intensity,
                "text": syllable["text"]
            })
            # add syllable dash
            if j > 0:
                lyrics.append({
                    "start": start,
                    "text": "--"
                })
            lyrics.append({
                "start": start,
                "text": syllable["text"]
            })

# Add non-words
for i, word in enumerate(data["nonwords"]):
    # add note
    if word["name"] in analysis and "primaryFrames" in analysis[word["name"]]:
        frames = analysis[word["name"]]["primaryFrames"]
        intensity = analysis[word["name"]]["maxIntensity"]
        start = int(round(word["start"] * 1000))
        end = int(round(word["end"] * 1000))
        notes.append({
            "notes": lilypond.framesToNotes(frames, start, end, minSlurMs, ADJUST_OCTAVE, MAX_OCTAVE),
            "start": start,
            "end": end,
            "intensity": intensity,
            "text": "x"
        })
        lyrics.append({
            "start": start,
            "text": "_"
        })
lyrics = sorted(lyrics, key=lambda l: l["start"])

# Normalize and print to lilypond syntax
notes = lilypond.normalizeNotes(notes, TEMPO, SHORTEST_NOTE)
notes = lilypond.addDynamics(notes, dynamics)
music["notes"] = notes
lilyString = lilypond.toString(music, lyrics, header, layout)

# pprint([(n["text"], n["note"]) for n in music["notes"][30:50]])
# sys.exit(1)

with open(args.OUTPUT_FILE, "w") as f:
    f.write(lilyString)
    print "Wrote %s notes to file %s" % (len(notes), args.OUTPUT_FILE)
