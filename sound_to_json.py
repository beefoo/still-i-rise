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
parser.add_argument('-out', dest="OUTPUT_FILE", default="annotate/data/still_i_rise.json", help="Path to output json file")

# init input
args = parser.parse_args()

data = {}
with open(args.INPUT_FILE) as f:
    data = json.load(f)

# Retrieve pitch data from Praat file
frames = fileToPitchData(args.PITCH_FILE)
print "%s frames read from file %s" % (len(frames), args.PITCH_FILE)

# Stats
ints = [f["intensity"] for f in frames]
freqs = [f["candidates"][0]["frequency"] for f in frames if len(f["candidates"]) > 0 and f["candidates"][0]["frequency"] > 0]
print "Freq [%s, %s] Intensities [%s, %s]" % (min(freqs), max(freqs), min(ints), max(ints))

# Add frequency value to frames
for i, f in enumerate(frames):
    freq = 0
    candidates = f["candidates"]
    if len(candidates) > 0:
        freq = candidates[0]["frequency"]
    frames[i]["frequency"] = freq

output = {
    "minFrequency": math.floor(min(freqs)),
    "maxFrequency": math.ceil(max(freqs)),
    "minIntensity": math.floor(min(ints)),
    "maxIntensity": math.ceil( max(ints)),
    "start": 0,
    "end": data["words"][-1]["end"]
}

groups = []
for i, line in enumerate(data["lines"]):
    groups.append({
        "name": line["name"],
        "text": line["text"],
        "type": "lines"
    })

dataOut = []
for i, word in enumerate(data["words"]):
    for j, syllable in enumerate(word["syllables"]):
        sFrames = [(f["start"], round(f["frequency"],2), round(f["intensity"],2)) for f in frames if syllable["start"] <= f["start"] < syllable["end"]]
        dataOut.append({
            "name": syllable["name"],
            "start": syllable["start"],
            "end": syllable["end"],
            "text": syllable["text"],
            "group": groups[word["line"]]["name"],
            "frames": sFrames
        })

for i, word in enumerate(data["nonwords"]):
    wFrames = [(f["start"], round(f["frequency"],2), round(f["intensity"],2)) for f in frames if word["start"] <= f["start"] < word["end"]]
    groups.append({
        "name": word["name"],
        "text": word["name"],
        "type": "nonwords"
    })
    dataOut.append({
        "name": word["name"],
        "start": word["start"],
        "end": word["end"],
        "text": "[non-word]",
        "group": word["name"],
        "frames": wFrames
    })

output["data"] = dataOut
output["groups"] = groups

with open(args.OUTPUT_FILE, 'w') as f:
    json.dump(output, f)

print "Done."
