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
parser.add_argument('-out', dest="OUTPUT_DIR", default="frames_motion/", help="Path to output directory")

# init input
args = parser.parse_args()

if not os.path.exists(args.OUTPUT_DIR):
    os.makedirs(args.OUTPUT_DIR)

frames = glob(args.INPUT_DIR)
frameCount = len(frames)
print "Found %s frames" % locale.format("%d", frameCount, grouping=True)
frames.sort()

cv2.ocl.setUseOpenCL(False) # https://github.com/opencv/opencv/issues/6081#issuecomment-198287324

fgbg = cv2.createBackgroundSubtractorMOG2()

# kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))
# fgbg = cv2.bgsegm.createBackgroundSubtractorGMG()

for i, f in enumerate(frames):
    im = cv2.imread(f)
    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (3, 3), 0)
    fgmask = fgbg.apply(blurred)
    # fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)
    cv2.imshow('frame',fgmask)
    cv2.waitKey(30)

cv2.destroyAllWindows()
