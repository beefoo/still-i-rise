# -*- coding: utf-8 -*-

import argparse
import json
from lib.midiutil.MidiFile import MIDIFile
from lib.praat import fileToPitchData
import sys

# input
parser = argparse.ArgumentParser()
parser.add_argument('-in', dest="INPUT_FILE", default="data/still_i_rise.json", help="Path to input aligned transcript json file")
parser.add_argument('-af', dest="ANALYSIS_FILE", default="data/still_i_rise_sound.json", help="Path to input sound analysis json file")
parser.add_argument('-out', dest="OUTPUT_FILE", default="data/still_i_rise.mid", help="Path to output midi file")
parser.add_argument('-bpm', dest="BPM", type=int, default=240, help="Beats per minute")
parser.add_argument('-mnd', dest="MIN_NOTE_DURATION", type=int, default=100, help="Minimum note duration in ms")

# init input
args = parser.parse_args()
BPM = args.BPM
MIN_NOTE_DURATION = args.MIN_NOTE_DURATION

data = {}
with open(args.INPUT_FILE) as f:
    data = json.load(f)

analysis = {}
with open(args.ANALYSIS_FILE) as f:
    analysis = json.load(f)
