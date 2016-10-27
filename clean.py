# -*- coding: utf-8 -*-

import argparse
import json
import os
from pprint import pprint
import sys
import time

# input
parser = argparse.ArgumentParser()
parser.add_argument('-in', dest="INPUT_FILE", default="data/and_still_i_rise_aligned.json", help="Path to input aligned transcript json file")
parser.add_argument('-out', dest="OUTPUT_FILE", default="data/and_still_i_rise_aligned.json", help="Path to output transcript json file")
parser.add_argument('-pr', dest="PRECISION", type=int, default=2, help="Precision of time")

# init input
args = parser.parse_args()
PRECISION = args.PRECISION

data = {}
with open(args.INPUT_FILE) as f:
    data = json.load(f)

words = data["words"]

for i, word in enumerate(words):
    # Round numbers
    start = round(word["start"], PRECISION)
    end = round(word["end"], PRECISION)
    # Round phones
    phones = word["phones"]
    for j, phone in enumerate(phones):
        phones[j]["duration"] = round(phone["duration"], PRECISION)
    # Check for duration diff
    duration = end - start
    phoneDuration = sum([p["duration"] for p in phones])
    diff = duration - phoneDuration
    if abs(diff) > (1.0/(PRECISION+1)):
        print "Duration discrepancy of %ss: <%s> (%s)" % (diff, word["alignedWord"], time.strftime('%M:%S', time.gmtime(start)))
    words[i]["start"] = start
    words[i]["end"] = end
    words[i]["phones"] = phones
    # Check for start/end overlap
    if i > 0 and words[i-1]["end"] > start:
        print "Time overlap of %ss: <%s> (%s)" % (words[i-1]["end"]-start, word["alignedWord"], time.strftime('%M:%S', time.gmtime(start)))

data["words"] = words

with open(args.OUTPUT_FILE, 'w') as f:
    json.dump(data, f, indent=2)

print "Done."
