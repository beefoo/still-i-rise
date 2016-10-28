# -*- coding: utf-8 -*-

# Description: generate audio clips for lines, words, and syllables

import argparse
import json
import os
from pprint import pprint
import re
import subprocess
import sys

# input
parser = argparse.ArgumentParser()
parser.add_argument('-in', dest="INPUT_FILE", default="data/and_still_i_rise_aligned.json", help="Path to input aligned transcript json file")
parser.add_argument('-au', dest="INPUT_AUDIO_FILE", default="and_still_i_rise.wav", help="Path to audio file file")
parser.add_argument('-out', dest="OUTPUT_DIR", default="clips/", help="Path to clip directory")
parser.add_argument('-min', dest="MIN_DURATION", type=float, default=0.1, help="Minimum duration of a clip")
parser.add_argument('-o', dest="OVERRIDE", type=int, default=0, help="Override existing syllable data")

# init input
args = parser.parse_args()
MIN_DURATION = args.MIN_DURATION
OVERRIDE = args.OVERRIDE
types = ["words", "syllables", "nonwords", "pauses"]

# create directories
if not os.path.exists(args.OUTPUT_DIR):
    os.makedirs(args.OUTPUT_DIR)
for t in types:
    if not os.path.exists(args.OUTPUT_DIR + t + "/"):
        os.makedirs(args.OUTPUT_DIR + t + "/")

data = {}
with open(args.INPUT_FILE) as f:
    data = json.load(f)

clips = []
words = data["words"]
nonwords = data["nonwords"]
pauses = data["pauses"]

def getName(prefix, i, obj):
    return "%s_%s_%s_%s" % (prefix, str(i).zfill(3), re.sub(r'\W+', '', word["alignedWord"], start))

for i, word in enumerate(words):
    start = int(word["start"])
    name = "word_%s_%s_%s" % (str(i).zfill(3), re.sub(r'\W+', '', word["alignedWord"]), start)
    word.update({"name": name, "type": "words"})
    clips.append(word)
    for j, syllable in enumerate(word["syllables"]):
        start = int(syllable["start"])
        name = "syll_%s_%s_%s_%s" % (str(i).zfill(3), j, re.sub(r'\W+', '', syllable["text"]), start)
        syllable.update({"name": name, "type": "syllables"})
        clips.append(syllable)

for i, word in enumerate(nonwords):
    start = int(word["start"])
    name = "nonword_%s_%s" % (str(i).zfill(3), start)
    word.update({"name": name, "type": "nonwords"})
    clips.append(word)

for i, word in enumerate(pauses):
    start = int(word["start"])
    name = "pause_%s_%s" % (str(i).zfill(3), start)
    word.update({"name": name, "type": "pauses"})
    clips.append(word)

for i, clip in enumerate(clips):
    fname = args.OUTPUT_DIR + clip["type"] + '/' + clip["name"] + '.wav'
    if os.path.isfile(fname) and not OVERRIDE:
        continue
    start = clip["start"]
    end = clip["end"]
    dur = end - start
    if dur < MIN_DURATION:
        end = round(start + MIN_DURATION, 2)
    command = ['ffmpeg', '-i', args.INPUT_AUDIO_FILE, '-ss', str(start), '-to', str(end), '-c', 'copy', fname]
    # print " ".join(command)
    subprocess.call(command)
