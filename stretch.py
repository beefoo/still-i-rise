# -*- coding: utf-8 -*-

import argparse
from pprint import pprint
from lib.paulstretch import stretch
import sys

# input
parser = argparse.ArgumentParser()
parser.add_argument('-in', dest="INPUT_FILE", default="still_i_rise.wav", help="Path to input audio file")
parser.add_argument('-mult', dest="MULTIPLY", type=float, default=3.0, help="Amount to multiply")
parser.add_argument('-out', dest="OUTPUT_FILE", default="output/still_i_rise_%sx.wav", help="Path to output audio file")

# init input
args = parser.parse_args()

stretch(args.INPUT_FILE, args.OUTPUT_FILE % int(round(args.MULTIPLY)), args.MULTIPLY)

print "Done."
