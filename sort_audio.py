# -*- coding: utf-8 -*-

# Description: sort audio clips by intensity, frequency, or duration; outputs .csv file for use in sequence.ck via ChucK
#   python sort_audio.py -sort syllables
#   python sort_audio.py -sort syllables -by frequency
#   python sort_audio.py -sort syllables -by duration -fixed 0

import argparse
import csv
import json
import os
from pprint import pprint
import sys
import time

# input
parser = argparse.ArgumentParser()
parser.add_argument('-in', dest="INPUT_FILE", default="data/still_i_rise.json", help="Path to input aligned transcript json file")
parser.add_argument('-out', dest="OUTPUT_FILE", default="data/ck_sequence.csv", help="Path to output csv sequence file")
parser.add_argument('-sort', dest="SORT_FIELD", default="words", help="Field to sort: syllables, words, or lines")
parser.add_argument('-by', dest="SORT_BY", default="intensity", help="Feature to sort by: intensity, frequency, or duration")
parser.add_argument('-dir', dest="SORT_DIRECTION", type=int, default=1, help="Sort direction: -1 or 1")
parser.add_argument('-overlap', dest="OVERLAP_MS", type=int, default=50, help="Amount of ms to overlap in clip")
parser.add_argument('-fixed', dest="FIXED_MS", type=int, default=200, help="Fixed ms to play each sound clip; set to 0 to disable")
parser.add_argument('-cd', dest="CLIP_DIR", default="clips/", help="Path to clip directory")
parser.add_argument('-fe', dest="FILE_EXT", default=".wav", help="File extension of audio clips")

# init input
args = parser.parse_args()
SORT_FIELD = args.SORT_FIELD
SORT_BY = args.SORT_BY
SORT_DIRECTION = args.SORT_DIRECTION
OVERLAP_MS = args.OVERLAP_MS
FIXED_MS = args.FIXED_MS
CLIP_DIR = args.CLIP_DIR
FILE_EXT = args.FILE_EXT

data = {}
with open(args.INPUT_FILE) as f:
    data = json.load(f)

# populate clips
clips = []
if SORT_FIELD in data:
    clips = data[SORT_FIELD]
if SORT_FIELD=="syllables":
    for word in data["words"]:
        clips += word["syllables"]

# add duration
for i, clip in enumerate(clips):
    clips[i]["duration"] = clip["end"] - clip["start"]

# sort clips
clips = sorted(clips, key=lambda c: SORT_DIRECTION * c[SORT_BY])

# generate a sequence
sequence = []
ms = 0
for clip in clips:
    dur = int(clip["duration"] * 1000)
    filename = CLIP_DIR + SORT_FIELD + "/" + clip["name"] + FILE_EXT
    if os.path.isfile(filename):
        sequence.append({
            "elapsed_ms": ms,
            "gain": 1.0,
            "file": filename
        })
    else:
        print "%s not found" % filename
    if FIXED_MS > 0:
        ms += FIXED_MS
    else:
        ms += dur - OVERLAP_MS
    ms = max(0, ms)

print "Total time: %s" % time.strftime('%M:%S', time.gmtime(ms/1000))

# Add milliseconds to sequence
elapsed = 0
for i, step in enumerate(sequence):
    sequence[i]['milliseconds'] = step['elapsed_ms'] - elapsed
    elapsed = step['elapsed_ms']

# Write sequence
with open(args.OUTPUT_FILE, 'wb') as f:
    w = csv.writer(f)
    for step in sequence:
        w.writerow([step['file']])
        w.writerow([step['gain']])
        w.writerow([step['milliseconds']])
    f.seek(-2, os.SEEK_END) # remove newline
    f.truncate()
    print "Successfully wrote sequence to file:  %s" % args.OUTPUT_FILE
