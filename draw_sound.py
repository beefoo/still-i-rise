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
parser.add_argument('-sf', dest="SOUND_FILE", default="clips/lines/line_000_1.wav", help="Path to input audio file")
parser.add_argument('-tf', dest="TEXT_FILE", default="textgrids/line_000_1.TextGrid", help="Path to input text file")
parser.add_argument('-out', dest="OUTPUT_FILE", default="data/line_000_1.eps", help="Path to output eps file")

# viewport/labels
parser.add_argument('-xaxis', dest="XAXIS", default="Time (s)", help="X-axis label")
parser.add_argument('-yaxis', dest="YAXIS", default="Frequency (Hz)", help="Y-axis label")
parser.add_argument('-tmaj', dest="TIME_MAJ_UNIT", default="0.5", help="X-axis (time) major unit")
parser.add_argument('-tmin', dest="TIME_MIN_UNIT", default="0.1", help="X-axis (time) minor unit")
parser.add_argument('-rb', dest="WIDTH", default="12", help="Width of figure (in)")

# spectrogram
parser.add_argument('-wl', dest="WINDOW_LENGTH", default="0.005", help="Window length (s)")
parser.add_argument('-mf', dest="MAX_FREQUENCY", default="5000.0", help="Maximum frequency (Hz)")
parser.add_argument('-ts', dest="TIME_STEP", default="0.005", help="Time step (s)")
parser.add_argument('-fs', dest="FREQUENCY_STEP", default="20.0", help="Frequency step (Hz)")
parser.add_argument('-ws', dest="WINDOW_SHAPE", default="Gaussian", help="Window shape")

# textgrid

# pitch
parser.add_argument('-dp', dest="DRAW_PITCH", default="yes", help="Should draw pitch?")
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
command = ['Praat', '--run', 'draw_sound.praat']
command += [args.SOUND_FILE, args.TEXT_FILE, args.OUTPUT_FILE]
command += [args.XAXIS, args.YAXIS, args.TIME_MAJ_UNIT, args.TIME_MIN_UNIT, args.WIDTH]
command += [args.WINDOW_LENGTH, args.MAX_FREQUENCY, args.TIME_STEP, args.FREQUENCY_STEP, args.WINDOW_SHAPE]
command += [args.DRAW_PITCH, args.PITCH_FLOOR, args.MAX_CANDIDATES, args.VERY_ACCURATE, args.SILENCE_THRESHOLD, args.VOICING_THRESHOLD, args.OCTAVE_COST, args.OCTAVE_JUMP_COST, args.VOICED_COST, args.PITCH_CEILING]
print "Running %s" % " ".join(command)
finished = subprocess.check_call(command)

print "Wrote data to %s" % args.OUTPUT_FILE
