import argparse
import json
import os
from lib.praat import dataToTextGrid
import sys

# input
parser = argparse.ArgumentParser()
parser.add_argument('-in', dest="INPUT_FILE", default="data/still_i_rise.json", help="Path to input aligned transcript json file")
parser.add_argument('-sf', dest="OUTPUT_DIR", default="textgrids", help="Path to textgrids dir")

# init input
args = parser.parse_args()

# create directory
if not os.path.exists(args.OUTPUT_DIR):
    os.makedirs(args.OUTPUT_DIR)

data = {}
with open(args.INPUT_FILE) as f:
    data = json.load(f)

lines = data["lines"]
words = data["words"]

for i, line in enumerate(lines):
    lineWords = [w for w in words if w["line"]==i]
    lineWords = sorted(lineWords, key=lambda w: w["start"])
    syllables = []
    lineStart = line["start"]
    for w in lineWords:
        for s in w["syllables"]:
            syllables.append({
                "xmin": s["start"] - lineStart,
                "xmax": s["end"] - lineStart,
                "text": s["text"]
            })
    fileContents = dataToTextGrid(syllables)
    fileName = args.OUTPUT_DIR + "/" + line["name"] + ".TextGrid"
    with open(fileName, "w") as f:
        f.write(fileContents)

print "Wrote %s lines to %s" % (len(lines), args.OUTPUT_DIR)
