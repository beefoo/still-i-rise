import argparse
import json
import math
import os
from pprint import pprint
from lib.praat import fileToPitchData
import sys

# input
parser = argparse.ArgumentParser()
parser.add_argument('-in', dest="INPUT_FILE", default="data/still_i_rise.json", help="Path to input aligned transcript json file")
parser.add_argument('-pf', dest="PITCH_FILE", default="data/still_i_rise.Pitch", help="Path to pitch file")
parser.add_argument('-out', dest="OUTPUT_FILE", default="data/still_i_rise_sound.json", help="Path to output json file")

# init input
args = parser.parse_args()

data = {}
with open(args.INPUT_FILE) as f:
    data = json.load(f)

# Retrieve pitch data from Praat file
pFrames = fileToPitchData(args.PITCH_FILE)
print "%s frames read from file %s" % (len(pFrames), args.PITCH_FILE)

def noteLabels():
    return ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

def freqToNote(freq):
    notes = noteLabels()
    A4 = 440
    C0 = A4 * math.pow(2, -4.75)
    h = int(round(12*(math.log(freq/C0)/math.log(2))))
    octave = int(h / 12) - 1
    octave = max(octave, 0)
    n = int(h % 12)
    note = notes[n]
    midi = max(((octave-1) * 12) + n, 0)
    return {
        "note": n,
        "octave": octave,
        "label": note + str(octave),
        "midi": midi
    }

def midiToNote(midi):
    notes = noteLabels()
    octave = int(midi / 12)
    n = int(midi % 12)
    note = notes[n]
    return {
        "note": n,
        "octave": octave,
        "label": note + str(octave),
        "midi": midi
    }

def getMaxIntensity(frames):
    intensities = [f["intensity"] for f in frames]
    return max(intensities)

def getNotes(frames):
    # no frames
    if len(frames) <= 0:
        return []
    # sort by time
    frames = sorted(frames, key=lambda f: f["start"])
    # too many frames, take last two frames
    if len(frames) > 2:
        frames = frames[-2:]

    notes = []
    # multiple frames, check for slur
    if len(frames) > 1:
        note1 = freqToNote(frames[0]["frequency"])
        note2 = freqToNote(frames[1]["frequency"])
        note1["intensity"] = frames[0]["intensity"]
        note2["intensity"] = frames[1]["intensity"]
        # same note, just add first
        if note1["midi"] == note2["midi"]:
            notes = [note1]
        # different note; make a slur
        else:
            notes = [note1, note2]
    # single note or notes not long enough for slur; take the first
    else:
        note = freqToNote(frames[0]["frequency"])
        note["intensity"] = frames[0]["intensity"]
        notes = [note]

    return notes

def groupCompare(a, b):
    aScore = a["size"] * a["intensity"]
    bScore = b["size"] * b["intensity"]
    if aScore < bScore:
        return 1
    elif bScore < aScore:
        return -1
    elif a["intensity"] < b["intensity"]:
        return 1
    elif b["intensity"] < a["intensity"]:
        return -1
    elif a["start"] < b["start"]:
        return 1
    elif b["start"] < a["start"]:
        return -1
    else:
        return 0

def getPrimaryFrames(frames, threshold=10):
    if len(frames) <= 0:
        return []

    # put frames into continuous groups
    groups = []
    group = []
    lastF = 0
    for frame in frames:
        f = frame["frequency"]
        delta = abs(f - lastF)
        # frame is continuation of last frame or is the first frame
        if f > 0 and (delta <= threshold or lastF <= 0):
            group.append(frame)
        # frame jumped high, add existing group, start a new group
        elif f > 0:
            if len(group):
                groups.append(group)
            group = [frame]
        # frame is silent, add existing group
        else:
            if len(group):
                groups.append(group)
            group = []
        lastF = f
    # add last group
    if len(group):
        groups.append(group)

    # map groups
    groups = [{
        "start": g[0]["start"],
        "intensity": sum([f["intensity"] for f in g]) / len(g),
        "size": len(g),
        "frames": g
    } for g in groups]

    # sort groups
    groups = sorted(groups, cmp=groupCompare)

    # select first group
    if len(groups) <= 0:
        return []
    frames = groups[0]["frames"];

    # sort by intensity, desc
    frames = sorted(frames, key=lambda f: -f["intensity"])

    # only take the most intense
    frames = frames[:int(math.ceil(len(frames)*0.5))]

    # sort by frequency, desc
    frames = sorted(frames, key=lambda f: -f["frequency"])

    # get frames before and after peak, sort by frequency asc
    maxFrame = frames[0]
    framesLeft = sorted([f for f in frames if f["start"] < maxFrame["start"]], key=lambda f: f["frequency"])
    framesRight = sorted([f for f in frames if f["start"] > maxFrame["start"]], key=lambda f: f["frequency"])

    # take the high and low
    frames = [maxFrame]
    if len(framesLeft):
        frames.append(framesLeft[0])
    if len(framesRight):
        frames.append(framesRight[0])

    # sort by time
    frames = sorted(frames, key=lambda f: f["start"])

    # map
    frames = [{
        "start": f["start"],
        "frequency": f["frequency"],
        "intensity": f["intensity"]
    } for f in frames]

    return frames

# Add frequency value to frames
for i, f in enumerate(pFrames):
    freq = 0
    candidates = f["candidates"]
    if len(candidates) > 0:
        freq = candidates[0]["frequency"]
    pFrames[i]["frequency"] = freq

# items are combination of syllables and nonwords
items = []
for i, word in enumerate(data["words"]):
    for j, syllable in enumerate(word["syllables"]):
        items.append(syllable)
items += data["nonwords"]

# build output
output = {}
for item in items:
    frames = [f for f in pFrames if item["start"] <= f["start"] < item["end"]]
    primaryFrames = getPrimaryFrames(frames)
    output[item["name"]] =  {
        "primaryFrames": primaryFrames,
        "maxIntensity": getMaxIntensity(frames),
        "notes": getNotes(primaryFrames)
    }

with open(args.OUTPUT_FILE, 'w') as f:
    json.dump(output, f)

print "Done."
