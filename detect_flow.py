# -*- coding: utf-8 -*-

# Based on:
#   http://docs.opencv.org/trunk/d7/d8b/tutorial_py_lucas_kanade.html
#   https://github.com/opencv/opencv/blob/master/samples/python/opt_flow.py
#
# Outputs image where direction responds to hue, length by brightness
#   0° Blue, 60° Magenta, 120° Red, 180° Yellow, 240° Green, 300° Cyan

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
parser.add_argument('-out', dest="OUTPUT_DIR", default="frames_flow/", help="Path to output directory")

# init input
args = parser.parse_args()

# if not os.path.exists(args.OUTPUT_DIR):
#     os.makedirs(args.OUTPUT_DIR)

def drawHsv(flow):
    h, w = flow.shape[:2]
    mag, ang = cv2.cartToPolar(flow[...,0], flow[...,1])
    hsv = np.zeros((h, w, 3), np.uint8)
    hsv[...,0] = ang*180/np.pi/2
    hsv[...,1] = 255
    hsv[...,2] = cv2.normalize(mag,None,0,255,cv2.NORM_MINMAX)
    bgr = cv2.cvtColor(hsv,cv2.COLOR_HSV2BGR)
    return bgr

frames = glob(args.INPUT_DIR)
frameCount = len(frames)
print "Found %s frames" % locale.format("%d", frameCount, grouping=True)
frames.sort()

prvs = None
for i, f in enumerate(frames):
    im = cv2.imread(f)

    if prvs is None:
        prvs = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
        continue

    nxt = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
    flow = cv2.calcOpticalFlowFarneback(prvs,nxt, None, 0.5, 3, 15, 3, 5, 1.2, 0)
    bgr = drawHsv(flow)
    cv2.imshow('frame',bgr)
    cv2.waitKey(30)
    prvs = nxt

cv2.destroyAllWindows()
