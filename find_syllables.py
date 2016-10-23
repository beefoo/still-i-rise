# -*- coding: utf-8 -*-

import argparse
import json
from nltk.corpus import cmudict
import os
from pprint import pprint
import sys

# input
parser = argparse.ArgumentParser()
parser.add_argument('-in', dest="INPUT_FILE", default="data/and_still_i_rise_aligned.json", help="Path to input aligned transcript json file")
parser.add_argument('-out', dest="OUTPUT_FILE", default="data/and_still_i_rise_aligned_syllables.json", help="Path to output transcript json file")
parser.add_argument('-o', dest="OVERRIDE", type=int, default=0, help="Override existing syllable data")

# init input
args = parser.parse_args()

data = {}
with open(args.INPUT_FILE) as f:
    data = json.load(f)

dictionary = cmudict.dict()

# matches = dictionary['history']
# pprint(matches)
# sys.exit(1)

words = data["words"]
wordCount = len(words)
print "Words found: %s" % wordCount

for i, entry in enumerate(words):
    if entry["phones"][0]["syllable"] and not args.OVERRIDE:
        sys.stdout.write('\r')
        sys.stdout.write(str(round(1.0*i/wordCount*100,3))+'%')
        sys.stdout.flush()
        continue
    word = entry["alignedWord"]
    try:
        matches = dictionary[word]
    except KeyError, e:
        matches = []
    if len(matches) >= 1:
        phones = matches[0]
        if len(phones) == len(entry["phones"]):
            syllableStart = 0
            for j, phone in enumerate(phones):
                # this phone is a syllable
                if phone[-1].isdigit():
                    data["words"][i]["phones"][syllableStart]["syllable"] = 1
                    syllableStart = j + 1
        else:
            print "Phones don't match for %s at %s seconds" % (word, entry["start"])
    else:
        print "Could not find %s at %s seconds" % (word, entry["start"])
    sys.stdout.write('\r')
    sys.stdout.write(str(round(1.0*i/wordCount*100,3))+'%')
    sys.stdout.flush()

with open(args.OUTPUT_FILE, 'w') as f:
    json.dump(data, f, indent=2)

print "Done."
