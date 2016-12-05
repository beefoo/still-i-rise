# -*- coding: utf-8 -*-

import argparse
import json
import math
import numpy as np
from lib.praat import fileToPitchData, fileToSpectrogramData
from PIL import Image, ImageDraw
from pprint import pprint
import random
import sys

# input
parser = argparse.ArgumentParser()
parser.add_argument('-in', dest="INPUT_FILE", default="data/still_i_rise.json", help="Path to input aligned transcript json file")
parser.add_argument('-sf', dest="SPECTROGRAM_FILE", default="data/still_i_rise.Spectrogram", help="Path to input spectrogram file")
parser.add_argument('-pf', dest="PITCH_FILE", default="data/still_i_rise.Pitch", help="Path to input pitch file")
parser.add_argument('-W', dest="WIDTH", type=int, default=800, help="Width of image")
parser.add_argument('-H', dest="HEIGHT", type=int, default=240, help="Height of image")
parser.add_argument('-l', dest="LINE", type=int, default=-1, help="Line to show")
parser.add_argument('-s', dest="START", type=int, default=0, help="Start in seconds")
parser.add_argument('-e', dest="END", type=int, default=5, help="End in seconds")
parser.add_argument('-dp', dest="DRAW_PITCH", type=int, default=0, help="Draw pitch? 1, 0")
parser.add_argument('-dt', dest="DRAW_TEXT", type=int, default=0, help="Draw text? 1, 0")

# init input
args = parser.parse_args()
WIDTH = args.WIDTH
HEIGHT = args.HEIGHT
START = args.START
END = args.END
DRAW_PITCH = (args.DRAW_PITCH > 0)
DRAW_TEXT = (args.DRAW_TEXT > 0)

data = {}
with open(args.INPUT_FILE) as f:
    data = json.load(f)

sData = fileToSpectrogramData(args.SPECTROGRAM_FILE)
print "Read %s steps from %s" % (len(sData["steps"]), args.SPECTROGRAM_FILE)

if DRAW_PITCH:
    pData = fileToPitchData(args.PITCH_FILE)
    print "%s frames read from file %s" % (len(pData), args.PITCH_FILE)

# Line
if args.LINE >= 0:
    START = data["lines"][args.LINE]["start"]
    END = data["lines"][args.LINE]["end"]

# Draw spectrogram
sFrames = [f for f in sData["steps"] if f["start"] >= START and f["end"] <= END]
nx = len(sFrames)
ny = int(sData["ny"])
dy = sData["dy"]
y1 = sData["y1"]
HEIGHT = min(HEIGHT, ny)
pixels = [(0,0,0)] * (WIDTH * HEIGHT)
for x, frame in enumerate(sFrames):
    fsteps = frame["fsteps"]
    ny = len(fsteps)
    fpp = sum(math.sqrt(f) for f in fsteps)
    for y, psd in enumerate(fsteps):
        px = 1.0 * x / nx
        py = 1.0 * y / ny
        ix = round(px * WIDTH)
        iy = round(py * HEIGHT)
        pxIndex = int(round(iy * WIDTH + ix))
        freq = y1 + dy * y
        # psd = Power Spectral Density in Amplitude^2/Hz.
        pp = math.sqrt(psd) / fpp
        color = int(round(pp * 255))
        colorTriple = (color, color, color)
        pixels[pxIndex] = colorTriple
im = Image.new("RGB", (WIDTH, HEIGHT))
im.putdata(pixels)
im.show()


# Draw pitches
# if DRAW_PITCH:

# Get syllables
if DRAW_TEXT:
    words = [w for w in data["words"] if w["start"] >= START and w["end"] <= END]
    syllables = []
    for w in words:
        for s in w["syllables"]:
            syllables.append(s)

    # Draw syllables
