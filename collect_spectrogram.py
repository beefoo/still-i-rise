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
parser.add_argument('-spec', dest="OUTPUT_FILE", default="data/still_i_rise.Spectrogram", help="Path to output spectrogram file")
parser.add_argument('-wl', dest="WINDOW_LENGTH", default="0.005", help="Window length (s)")
parser.add_argument('-mf', dest="MAX_FREQUENCY", default="4000.0", help="Maximum frequency (Hz)")
parser.add_argument('-ts', dest="TIME_STEP", default="0.005", help="Time step (s)")
parser.add_argument('-fs', dest="FREQUENCY_STEP", default="40.0", help="Frequency step (Hz)")
parser.add_argument('-ws', dest="WINDOW_SHAPE", default="Gaussian", help="Window shape")

# init input
args = parser.parse_args()

# cut the clip
command = ['Praat', '--run', 'collect_spectrogram.praat', args.INPUT_FILE, args.OUTPUT_FILE, args.WINDOW_LENGTH, args.MAX_FREQUENCY, args.TIME_STEP, args.FREQUENCY_STEP, args.WINDOW_SHAPE]
print "Running %s" % " ".join(command)
finished = subprocess.check_call(command)

print "Wrote data to %s" % args.OUTPUT_FILE
