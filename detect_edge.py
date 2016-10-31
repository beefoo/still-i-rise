# -*- coding: utf-8 -*-

import argparse
import cv2
import locale
import os
from glob import glob
import numpy as np
from PIL import Image
from pprint import pprint
import sys

locale.setlocale(locale.LC_ALL, 'en_US')

# input
parser = argparse.ArgumentParser()
parser.add_argument('-in', dest="INPUT_DIR", default="frames/*.png", help="Path to frames directory")
parser.add_argument('-out', dest="OUTPUT_DIR", default="frames_edge/", help="Path to output directory")

# init input
args = parser.parse_args()

if not os.path.exists(args.OUTPUT_DIR):
    os.makedirs(args.OUTPUT_DIR)

frames = glob(args.INPUT_DIR)
frameCount = len(frames)
print "Found %s frames" % locale.format("%d", frameCount, grouping=True)
frames.sort()

for i, f in enumerate(frames):
    im = cv2.imread(f)
    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (3, 3), 0)
    edges = cv2.Canny(blurred,100,100)
    cv2.imshow('frame',edges)
    cv2.waitKey(30)

cv2.destroyAllWindows()
