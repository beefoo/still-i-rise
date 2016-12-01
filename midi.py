# -*- coding: utf-8 -*-

import argparse
import json
from lib.midiutil.MidiFile import MIDIFile
from pprint import pprint
from lib.praat import fileToPitchData
import math
import sys

# input
parser = argparse.ArgumentParser()
parser.add_argument('-in', dest="INPUT_FILE", default="data/still_i_rise.json", help="Path to input aligned transcript json file")
parser.add_argument('-af', dest="ANALYSIS_FILE", default="data/still_i_rise_sound.json", help="Path to input sound analysis json file")
parser.add_argument('-out', dest="OUTPUT_FILE", default="data/still_i_rise.mid", help="Path to output midi file")
parser.add_argument('-bpm', dest="BPM", type=int, default=240, help="Beats per minute")
parser.add_argument('-pad', dest="NOTE_PADDING", type=int, default=120, help="Ms to add to end of each note")
parser.add_argument('-vm', dest="VOLUME_MULTIPLIER", type=float, default=2.0, help="Increase/decrease volume by this multiplier")
parser.add_argument('-slr', dest="SLUR", type=int, default=0, help="Slur (0) or don't slur (1)")

# init input
args = parser.parse_args()
BPM = args.BPM
NOTE_PADDING = args.NOTE_PADDING
VOLUME_MULTIPLIER = args.VOLUME_MULTIPLIER
SLUR = args.SLUR

data = {}
with open(args.INPUT_FILE) as f:
    data = json.load(f)

analysis = {}
with open(args.ANALYSIS_FILE) as f:
    analysis = json.load(f)

def msToBeats(ms, bpm):
    bpms = 1.0 * bpm / 60 / 1000
    return bpms * ms

def notesToSteps(notes, start, end, slur=1):
    steps = []
    dur = end - start
    # more than one note; slur
    if len(notes) > 1 and slur:
        # midi step
        midiStart = int(notes[0]["midi"])
        midiEnd = int(notes[1]["midi"])
        midiDiff = midiEnd - midiStart
        stepCount = abs(midiDiff)+1
        midiStep = int(1.0 * midiDiff / stepCount)
        midi = midiStart
        # time step
        stepDur = int(1.0 * dur / stepCount)
        ms = start
        # intensity step
        istart = notes[0]["intensity"]
        iend = notes[1]["intensity"]
        idiff = iend - istart
        istep = idiff / stepCount
        intensity = istart
        # do steps
        for i in range(stepCount):
            steps.append({
                "ms": ms,
                "dur": stepDur,
                "pitch": midi,
                "volume": int(round(intensity*100))
            })
            ms += stepDur
            midi += midiStep
            intensity += istep
    # only one note
    elif len(notes) > 0:
        steps.append({
            "ms": start,
            "dur": dur,
            "pitch": notes[0]["midi"],
            "volume": int(round(notes[0]["intensity"]*100))
        })
    return steps


# items are combination of syllables and nonwords
items = []
for word in data["words"]:
    for syllable in word["syllables"]:
        items.append(syllable)
items += data["nonwords"]

# build midi sequence
sequence = []
for item in items:
    name = item["name"]
    if name in analysis:
        notes = analysis[name]["notes"]
        start = int(item["start"] * 1000)
        end = int(item["end"] * 1000)
        steps = notesToSteps(notes, start, end, SLUR)
        for step in steps:
            sequence.append(step)

# pprint(sequence[:10])
# sys.exit(1)

# write sequence to midi file
if len(sequence) > 0:
    # Create the MIDIFile Object with 1 track
    MyMIDI = MIDIFile(1)

    # Tracks are numbered from zero. Times are measured in beats.
    track = 0
    time = 0
    channel = 0

    # Add track name and tempo.
    MyMIDI.addTrackName(track,time,"Track")
    MyMIDI.addTempo(track,time,BPM)

    # Now add the note.
    for step in sequence:
        pitch = step["pitch"]
        time = msToBeats(step["ms"],BPM)
        duration = msToBeats(step["dur"]+NOTE_PADDING,BPM)
        volume = int(min(VOLUME_MULTIPLIER * step["volume"], 100))
        MyMIDI.addNote(track,channel,pitch,time,duration,volume)

    # And write it to disk
    with open(args.OUTPUT_FILE, 'wb') as f:
        MyMIDI.writeFile(f)
        print("Successfully wrote to file: %s" % args.OUTPUT_FILE)
