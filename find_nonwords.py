# -*- coding: utf-8 -*-

import argparse
import json
import locale
import os
from pprint import pprint
from praat import fileToPulseData
import sys
import time

# input
parser = argparse.ArgumentParser()
parser.add_argument('-in', dest="INPUT_FILE", default="data/and_still_i_rise_aligned.json", help="Path to input aligned transcript json file")
parser.add_argument('-pf', dest="PULSE_FILE", default="data/and_still_i_rise.PointProcess", help="Path to pulse file")
parser.add_argument('-out', dest="OUTPUT_FILE", default="data/and_still_i_rise_aligned.json", help="Path to output json file")
parser.add_argument('-md', dest="MIN_DURATION", type=float, default=0.1, help="Path to output json file")

# init input
args = parser.parse_args()
MIN_DURATION = args.MIN_DURATION

data = {}
with open(args.INPUT_FILE) as f:
    data = json.load(f)

# Retrieve pulse data from Praat file
rawPulses = fileToPulseData(args.PULSE_FILE)
print "%s raw pulses read from file %s" % (locale.format("%d", len(rawPulses), grouping=True), args.PULSE_FILE)

# Process pulses in pulse blocks
pulses = []
p0 = rawPulses.pop(0)
p = p0
for rp in rawPulses:
    diff = rp - p
    if diff >= MIN_DURATION:
        if (p-p0) >= MIN_DURATION:
            pulses.append((p0, p))
        p0 = rp
    p = rp
if (p-p0) >= MIN_DURATION:
    pulses.append((p0, p))
print "%s pulses found" % len(pulses)

# pprint(pulses)
# sys.exit(1)

# Look for gaps
words = data["words"]
prev = 0
gaps = []
for word in words:
    start = word["start"]
    end = word["end"]
    diff = start - prev
    if diff >= MIN_DURATION:
        gaps.append((prev, start))
    prev = end

print "Found %s gaps over %ss" % (len(gaps), MIN_DURATION)

# pprint(gaps)
# sys.exit(1)

# Analyze gaps for nonwords and pauses
nonwords = []
pauses = []
for gap in gaps:
    g0 = gap[0]
    g1 = gap[1]
    # Check for pulses in gap
        # Case: Either end of the pulse is contained in the gap
        # Case: The pulse spans the entire gap
    gapPulses = [p for p in pulses if p[1] > g0 and p[1] < g1 or p[0] > g0 and p[0] < g1 or p[0] <= g0 and p[1] >= g1]
    # Add nonwords, pauses
    start = g0
    for p in gapPulses:
        p0 = p[0]
        p1 = p[1]
        # pause found
        if p0 > start and (p0-start) >= MIN_DURATION:
            pauses.append({"start": start, "end": p0})
        nonwords.append({"start": max(p0, g0), "end": min(p1, g1)})
        start = p1
    # No pulses; add as a pause
    if len(gapPulses) <= 0:
        pauses.append({"start": g0, "end": g1})

data["nonwords"] = nonwords
data["pauses"] = pauses
print "Found %s nonwords and %s pauses" % (len(nonwords), len(pauses))

pprint(nonwords[0:min(10, len(nonwords))])

# with open(args.OUTPUT_FILE, 'w') as f:
#     json.dump(data, f, indent=2)
#
# print "Done."
