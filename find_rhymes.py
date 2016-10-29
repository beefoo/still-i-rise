# -*- coding: utf-8 -*-

import argparse
import json
import os
from pprint import pprint
import sys
import time

# input
parser = argparse.ArgumentParser()
parser.add_argument('-in', dest="INPUT_FILE", default="data/still_i_rise.json", help="Path to input aligned transcript json file")
parser.add_argument('-out', dest="OUTPUT_FILE", default="data/still_i_rise_rhymes.json", help="Path to output rhymes json file")

# init input
args = parser.parse_args()

data = {}
with open(args.INPUT_FILE) as f:
    data = json.load(f)

words = data["words"]

rhymeGroups = []

for word in words:
    phones = word["phones"]
    vowels = [p["phone"].split('_')[0] for p in phones if p["phone"][0].lower() in ["a","e","i","o","u"]]
    if len(vowels) > 2:
        vowels = vowels[-2:]
    pattern = "_".join(vowels)
    rhymeGroup = next((g for g in rhymeGroups if g["pattern"]==pattern), None)
    if rhymeGroup:
        rhymeGroup["words"].append(word["alignedWord"])
        rhymeGroups[rhymeGroup["index"]] = rhymeGroup
    else:
        rhymeGroup = {
            "index": len(rhymeGroups),
            "pattern": pattern,
            "words": [word["alignedWord"]]
        }
        rhymeGroups.append(rhymeGroup)

rhymeGroups = sorted(rhymeGroups, key=lambda g: -len(g["words"]))

# pprint(rhymeGroups)
print "%s rhyme groups found" % len(rhymeGroups)

with open(args.OUTPUT_FILE, 'w') as f:
    json.dump(rhymeGroups, f, indent=2)

print "Done."
