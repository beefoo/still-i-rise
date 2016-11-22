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
parser.add_argument('-in', dest="INPUT_FILE", default="data/still_i_rise.json", help="Path to input aligned transcript json file")
parser.add_argument('-au', dest="INPUT_AUDIO_FILE", default="still_i_rise.wav", help="Path to audio file file")
parser.add_argument('-out', dest="OUTPUT_DIR", default="clips/", help="Path to clip directory")
parser.add_argument('-min', dest="MIN_DURATION", type=float, default=0.1, help="Minimum duration of a clip")
parser.add_argument('-pa', dest="PAD", type=float, default=0.02, help="Amount of seconds to pad before and after")
parser.add_argument('-fa', dest="FADE", type=float, default=0.02, help="Amount of seconds to fade before and after")
parser.add_argument('-o', dest="OVERRIDE", type=int, default=0, help="Override existing syllable data")
parser.add_argument('-fe', dest="FILE_EXT", default=".wav", help="File extension of audio clips")

# init input
args = parser.parse_args()
MIN_DURATION = args.MIN_DURATION
PAD = args.PAD
FADE = args.FADE
OVERRIDE = args.OVERRIDE
FILE_EXT = args.FILE_EXT
types = ["lines", "words", "syllables", "nonwords", "pauses"]

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
lines = data["lines"]
words = data["words"]
nonwords = data["nonwords"]
pauses = data["pauses"]

# create clips

for i, line in enumerate(lines):
    line.update({"type": "lines"})
    clips.append(line)

for i, word in enumerate(words):
    word.update({"type": "words"})
    clips.append(word)
    for j, syllable in enumerate(word["syllables"]):
        syllable.update({"type": "syllables"})
        clips.append(syllable)

for i, word in enumerate(nonwords):
    word.update({"type": "nonwords"})
    clips.append(word)

for i, word in enumerate(pauses):
    word.update({"type": "pauses"})
    clips.append(word)

# generate clips

for i, clip in enumerate(clips):
    fname = args.OUTPUT_DIR + clip["type"] + '/' + clip["name"] + FILE_EXT
    fnameTmp = args.OUTPUT_DIR + clip["type"] + '/' + clip["name"] + "_temp" + FILE_EXT
    if os.path.isfile(fname) and not OVERRIDE:
        continue
    start = max(round(clip["start"] - PAD, 2), 0)
    end = round(clip["end"] + PAD, 2)
    dur = end - start
    if dur < MIN_DURATION:
        end = round(start + MIN_DURATION, 2)

    # cut the clip
    command = ['ffmpeg', '-i', args.INPUT_AUDIO_FILE, '-ss', str(start), '-to', str(end), '-c', 'copy', fnameTmp, '-y']
    # print " ".join(command)
    finished = subprocess.check_call(command)

    # fade the clip
    st = round(end - start - FADE, 2)
    command = ['ffmpeg', '-i', fnameTmp, '-af', "afade=t=in:ss=0:d="+str(FADE)+",afade=t=out:st="+str(st)+":d="+str(FADE), fname, '-y']
    # print " ".join(command)
    finished = subprocess.check_call(command)

    # delete temp file
    os.remove(fnameTmp)
