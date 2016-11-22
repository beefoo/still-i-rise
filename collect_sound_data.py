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
parser.add_argument('-in', dest="INPUT_FILE", default="still_i_rise.wav", help="Path to input audio file file")
parser.add_argument('-pitch', dest="OUTPUT_PITCH_FILE", default="data/still_i_rise.Pitch", help="Path to output pitch data file")
parser.add_argument('-pulse', dest="OUTPUT_PULSE_FILE", default="data/still_i_rise.PointProcess", help="Path to output pulse data file")
parser.add_argument('-ts', dest="TIME_STEP", default="0.01", help="Time step in seconds")
parser.add_argument('-p0', dest="PITCH_FLOOR", default="70", help="Pitch floor in Hz")
parser.add_argument('-mc', dest="MAX_CANDIDATES", default="4", help="Maximum candidates per frame")
parser.add_argument('-va', dest="VERY_ACCURATE", default="on", help="Very accurate, on/off")
parser.add_argument('-st', dest="SILENCE_THRESHOLD", default="0.01", help="Silence threshold")
parser.add_argument('-vt', dest="VOICING_THRESHOLD", default="0.3", help="Voicing threshold")
parser.add_argument('-oc', dest="OCTAVE_COST", default="0.001", help="Octave cost")
parser.add_argument('-ojc', dest="OCTAVE_JUMP_COST", default="0.3", help="Octave jump cost")
parser.add_argument('-vc', dest="VOICED_COST", default="0.2", help="Voiced cost")
parser.add_argument('-p1', dest="PITCH_CEILING", default="400", help="Pitch ceiling in Hz")

# init input
args = parser.parse_args()

# cut the clip
command = ['Praat', '--run', 'collect_sound_data.praat', args.INPUT_FILE, args.OUTPUT_PITCH_FILE, args.OUTPUT_PULSE_FILE, args.TIME_STEP, args.PITCH_FLOOR, args.MAX_CANDIDATES, args.VERY_ACCURATE, args.SILENCE_THRESHOLD, args.VOICING_THRESHOLD, args.OCTAVE_COST, args.OCTAVE_JUMP_COST, args.VOICED_COST, args.PITCH_CEILING]
print "Running %s" % " ".join(command)
finished = subprocess.check_call(command)

print "Wrote data to %s" % args.OUTPUT_PITCH_FILE
