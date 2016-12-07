# -*- coding: utf-8 -*-

# Description: add lines, verses to aligned transcript

import argparse
import json
import os
from pprint import pprint
import sys

# input
parser = argparse.ArgumentParser()
parser.add_argument('-in', dest="INPUT_FILE", default="data/still_i_rise.json", help="Path to input aligned transcript json file")
parser.add_argument('-out', dest="OUTPUT_FILE", default="data/still_i_rise.json", help="Path to output aligned transcript json file")

# init input
args = parser.parse_args()

data = {}
with open(args.INPUT_FILE) as f:
    data = json.load(f)

transcript = data["transcript"]
words = data["words"]
lines = []
verses = []

def getLineOrVerse(t,i,ws):
    global transcript
    w0 = ws[0]
    w1 = ws[-1]
    endOffset = w1["endOffset"]
    # include ending punctuation
    while transcript[endOffset] != "\r" and endOffset < len(transcript)-1:
        endOffset += 1
    text = transcript[w0["startOffset"]:endOffset]
    name = "%s_%s_%s" % (t, str(i).zfill(3), int(w0["start"]))
    return {
        "text": text,
        "name": name,
        "startOffset": w0["startOffset"],
        "endOffset": endOffset,
        "start": w0["start"],
        "end": w1["end"]
    }

line = []
verse = []
for wi, word in enumerate(words):
    prev = ""
    if wi > 0:
        word0 = words[wi - 1]
        prev = transcript[word0["endOffset"]:word["startOffset"]]
    # Check for new verse
    if "\r\n\r\n" in prev:
        verses.append(getLineOrVerse("verse", len(verses), verse))
        verse = []
    # Check for new line
    if "\r\n" in prev:
        lines.append(getLineOrVerse("line", len(lines), line))
        line = []
    data["words"][wi]["verse"] = len(verses)
    data["words"][wi]["line"] = len(lines)
    verse.append(word)
    line.append(word)
verses.append(getLineOrVerse("verse", len(verses), verse))
lines.append(getLineOrVerse("line", len(lines), line))

data["verses"] = verses
data["lines"] = lines

with open(args.OUTPUT_FILE, 'w') as f:
    json.dump(data, f, indent=2)

print "Done."
