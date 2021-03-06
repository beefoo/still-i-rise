# -*- coding: utf-8 -*-

# Based on: http://docs.opencv.org/trunk/da/d22/tutorial_py_canny.html

import argparse
import cv2
import locale
import os
from glob import glob
import numpy as np
from pprint import pprint
import sys

try:
    locale.setlocale(locale.LC_ALL, 'en_US')
except locale.Error:
    locale.setlocale(locale.LC_ALL, 'english-us')

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
