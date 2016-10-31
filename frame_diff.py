# -*- coding: utf-8 -*-

import argparse
import locale
import os
from glob import glob
from PIL import Image
from pprint import pprint
import sys

locale.setlocale(locale.LC_ALL, 'en_US')

# input
parser = argparse.ArgumentParser()
parser.add_argument('-in', dest="INPUT_DIR", default="frames/*.png", help="Path to frames directory")
parser.add_argument('-out', dest="OUTPUT_DIR", default="frames_diff/", help="Path to output directory")

# init input
args = parser.parse_args()

if not os.path.exists(args.OUTPUT_DIR):
    os.makedirs(args.OUTPUT_DIR)

def pixelsEquals(px0, px1, tolerance=2.0):
    return abs(px0[0]-px1[0]) < tolerance and abs(px0[1]-px1[1]) < tolerance and abs(px0[2]-px1[2]) < tolerance

def getImagePixels(filename):
    im = Image.open(filename)
    pixels = list(im.getdata())
    width, height = im.size
    pixels = [pixels[i * width:(i + 1) * width] for i in xrange(height)]
    return (pixels, width, height)

def getPixelDiff(px0, px1):
    diff = []
    for i, row in enumerate(px1):
        for j, px in enumerate(row):
            if pixelsEquals(px0[i][j], px):
                diff.append((0,0,0))
            else:
                diff.append((255,255,255))
    return diff

def pxToImage(pxs, w, h, filename):
    im = Image.new('RGB', (w, h))
    im.putdata(pxs)
    im.save(filename)

frames = glob(args.INPUT_DIR)
frameCount = len(frames)
print "Found %s frames" % locale.format("%d", frameCount, grouping=True)
frames.sort()

px0 = None
w = None
h = None
for i, f in enumerate(frames):
    if i <= 0:
        (px0, w, h) = getImagePixels(f)
        continue
    (px1, w, h) = getImagePixels(f)
    diff = getPixelDiff(px0, px1)
    filename = args.OUTPUT_DIR + frames[i-1].split('/')[-1]
    pxToImage(diff, w, h, filename)
    px0 = px1
    sys.stdout.write('\r')
    sys.stdout.write(str(round(1.0*i/frameCount*100,3))+'%')
    sys.stdout.flush()

print "Done."
