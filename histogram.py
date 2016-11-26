# -*- coding: utf-8 -*-

import argparse
import json
import matplotlib
import matplotlib.pyplot as plt
import sys

parser = argparse.ArgumentParser()
parser.add_argument('-in', dest="INPUT_FILE", default="data/still_i_rise_sound.json", help="Path to input sound analysis json file")
parser.add_argument('-key', dest="KEY", default="intensity", help="Key to output, e.g. instensity, frequency, duration")

# init input
args = parser.parse_args()
KEY = args.KEY

data = {}
with open(args.INPUT_FILE) as f:
    data = json.load(f)

x = []
for key in data:
    for f in data[key]["primaryFrames"]:
        value = f[KEY]
        x.append(value)

# Make a normed histogram
plt.hist(x, bins=100, normed=True)

plt.show()
