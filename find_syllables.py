# -*- coding: utf-8 -*-

import argparse
import json
from lib.hyphenate import hyphenate_word
from nltk.corpus import cmudict
import os
from pprint import pprint
import sys
import time

# input
parser = argparse.ArgumentParser()
parser.add_argument('-in', dest="INPUT_FILE", default="data/still_i_rise.json", help="Path to input aligned transcript json file")
parser.add_argument('-out', dest="OUTPUT_FILE", default="data/still_i_rise.json", help="Path to output transcript json file")
parser.add_argument('-o', dest="OVERRIDE", type=int, default=0, help="Override existing syllable data")
parser.add_argument('-pr', dest="PRECISION", type=int, default=2, help="Precision of time")

# init input
args = parser.parse_args()
PRECISION = args.PRECISION

overrides = {
    "very": ["ve", "ry"],
    "sassiness": ["sa", "ssi", "ness"],
    "falling": ["fal", "ling"],
    "teardrops": ["tear", "drops"],
    "diamonds": ["dia", "monds"],
    "ocean": ["o", "cean"],
    "welling": ["wel", "ling"],
    "swelling": ["swel", "ling"],
    "into": ["in", "to"],
    "miraculously": ["mi", "ra", "cu", "lous", "ly"]
}

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
            print "Phones don't match for <%s> at %s" % (word, time.strftime('%M:%S', time.gmtime(entry["start"])))
    else:
        print "Could not find %s at %s" % (word, time.strftime('%M:%S', time.gmtime(entry["start"])))
    sys.stdout.write('\r')
    sys.stdout.write(str(round(1.0*i/wordCount*100,3))+'%')
    sys.stdout.flush()

# Now split word into syllables using hyphenator
words = data["words"]
for i, entry in enumerate(words):
    word = entry["alignedWord"]
    syllables1 = hyphenate_word(word)
    syllables2 = [p for p in entry["phones"] if "syllable" in p]

    if word in overrides:
        syllables1 = overrides[word]

    # Syllables match
    if len(syllables1) == len(syllables2):
        start = entry["start"]
        dur = 0
        syllables = []
        text = ""
        for ip, p in enumerate(entry['phones']):
            text = syllables1[len(syllables)]
            # Syllable start
            if "syllable" in p:
                if dur > 0:
                    syllables.append({
                        "name": "syll_%s_%s_%s_%s" % (str(i).zfill(3), len(syllables), re.sub(r'\W+', '', text), int(start)),
                        "text": text,
                        "start": start,
                        "end": round(start + dur, PRECISION)
                    })
                start += dur
                dur = 0
            dur += p["duration"]
        if dur > 0:
            text = syllables1[len(syllables)]
            syllables.append({
                "name": "syll_%s_%s_%s_%s" % (str(i).zfill(3), len(syllables), re.sub(r'\W+', '', text), int(start)),
                "text": text,
                "start": start,
                "end": round(start + dur, PRECISION)
            })
        words[i]["syllables"] = syllables
    # Syllables don't match
    elif "syllables" not in word:
        print "Hyphenator's syllables don't match for <%s> at %s" % (word, time.strftime('%M:%S', time.gmtime(entry["start"])))
        pprint(syllables1)

data["words"] = words

with open(args.OUTPUT_FILE, 'w') as f:
    json.dump(data, f, indent=2)

print "Done."
