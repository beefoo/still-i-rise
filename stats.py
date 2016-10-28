# -*- coding: utf-8 -*-

import argparse
import json
import os
from pprint import pprint
import sys

# input
parser = argparse.ArgumentParser()
parser.add_argument('-in', dest="INPUT_FILE", default="data/and_still_i_rise_aligned.json", help="Path to input aligned transcript json file")
parser.add_argument('-min', dest="MIN_DURATION", type=float, default=0.08, help="Minimum duration of a clip")

# init input
args = parser.parse_args()
minDuration = args.MIN_DURATION

data = {}
with open(args.INPUT_FILE) as f:
    data = json.load(f)

words = data["words"]
wordsValid = []
syllablesValid = []
wordsInvalid = []
syllablesInvalid = []

for word in words:
    duration = word["end"] - word["start"]
    if duration >= minDuration:
        wordsValid.append((word["word"], duration))
    else:
        wordsInvalid.append((word["word"], duration))
    for syllable in word["syllables"]:
        duration = syllable["end"] - syllable["start"]
        if duration >= minDuration:
            syllablesValid.append((syllable["text"], duration))
        else:
            syllablesInvalid.append((syllable["text"], duration))

print "Min duration: %s" % minDuration
print "Words: %s" % len(words)
print "--Valid: %s" % len(wordsValid)
print "--Invalid: %s" % len(wordsInvalid)
pprint(wordsInvalid)
print "-----"
print "Syllables: %s" % (len(syllablesValid) + len(syllablesInvalid))
print "--Valid: %s" % len(syllablesValid)
print "--Invalid: %s" % len(syllablesInvalid)
pprint(syllablesInvalid)
print "Non-words: %s" % len(data["nonwords"])
print "Pauses: %s" % len(data["pauses"])
print "Total clips: %s" % (len(words) + len(syllablesValid) + len(syllablesInvalid) + len(data["nonwords"]) + len(data["pauses"]))
